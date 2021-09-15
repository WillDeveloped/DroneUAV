import torch
import cv2
import time
import argparse
import numpy as np


from torchvision.transforms import Compose
from model.dpt_depth import DPTDepthModel
from model.midas_net import MidasNet
from model.midas_net_custom import MidasNet_small
from model.transforms import Resize, NormalizeImage, PrepareForNet

start_time = time.time()


torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True
optimized = True


#select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device: %s" % device)
#load network
model = DPTDepthModel(
        path="Resources\dpt_large-midas-2f21e586.pt",
        backbone="vitl16_384",
        non_negative=True,        )
net_w, net_h = 384, 384
resize_mode = "minimal"
normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])

transform = Compose(
    [
        Resize(
            net_w,
            net_h,
            resize_target=None,
            keep_aspect_ratio=True,
            ensure_multiple_of=32,
            resize_method=resize_mode,
            image_interpolation_method=cv2.INTER_CUBIC,
        ),
        normalization,
        PrepareForNet(),
    ]
)

model.eval()

if optimized and torch.device("cuda"):
    model = model.to(memory_format=torch.channels_last)  
    model = model.half()
        

model.to(device)
    


def classify(img):
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) / 255.0

    img_input = transform({"image": img})["image"]

    with torch.no_grad():
        sample = torch.from_numpy(img_input).to(device).unsqueeze(0)
        if optimized==True and device == torch.device("cuda"):
                sample = sample.to(memory_format=torch.channels_last)  
                sample = sample.half()

        prediction = model.forward(sample)
        prediction = (
                torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=img.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                )
                .squeeze()
                .cpu()
                .numpy()
            )
        

        bits = 2
        depth_min = prediction.min()
        depth_max = prediction.max()

        max_val = (2**(8*bits))-1

        if depth_max - depth_min > np.finfo("float").eps:
            out = max_val * (prediction - depth_min) / (depth_max - depth_min)
        else:
            out = np.zeros(prediction.shape, dtype=prediction.type)

        return out.astype("uint16")

def main():
    img = cv2.imread("test.jpg")
    classifiedImage = classify(img)
    print("#####---%s seconds ---#####" % (time.time() - start_time))
    cv2.imwrite("face.png", classifiedImage)
    cv2.imshow("image",classifiedImage)
    cv2.waitKey()


if __name__ == "__main__":  
    main()