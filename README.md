## <p align="center"><a href="https://arxiv.org/abs/2308.07946">[📄 Paper]</a> DSFNet:  Convolutional Encoder-Decoder Architecture Combined Dual-GCN and Stand-alone Self-attention by Fast Normalized Fusion for Polyps Segmentation
<p align="center"><img src='./overall.png'  width=800></p>

## 📖 Abstract
In the past few decades, deep learning technology has been widely used in medical image segmentation and has made significant breakthroughs in the fields of liver and liver tumor segmentation, brain and brain tumor segmentation, video disc segmentation, heart image segmentation, and so on. However, the segmentation of polyps is still a challenging task since the surface of the polyps is flat and the color is very similar to that of surrounding tissues. Thus, It leads to the problems of the unclear boundary between polyps and surrounding mucosa, local overexposure, and bright spot reflection. To counter this problem, this paper presents a novel U-shaped network, namely DSFNet, which effectively combines the advantages of Dual-GCN and self-attention mechanisms. First, we introduce a feature enhancement block module based on Dual-GCN module as an attention mechanism to enhance the feature extraction of local spatial and structural information with fine granularity. Second, the stand-alone self-attention module is designed to enhance the integration ability of the decoding stage model to global information. Finally, the Fast Normalized Fusion method with trainable weights is used to efficiently fuse the corresponding three feature graphs in encoding, bottleneck, and decoding blocks, thus promoting information transmission and reducing the semantic gap between encoder and decoder. Our model is tested on two public datasets including Endoscene and Kvasir-SEG and compared with other state-of-the-art models. Experimental results show that the proposed model surpasses other competitors in many indicators, such as Dice, MAE, and IoU. In the meantime, ablation studies are also conducted to verify the efficacy and effectiveness of each module. Qualitative and quantitative analysis indicates that the proposed model has great clinical significance.

## 💡 Highlights
- We propose a Dual-GCN based feature enhancement block module as an attention mechanism to the bottleneck of the U-shaped network in enhancing the feature extraction of local spatial and structural information of the image.

- We use stand-alone self-attention module to enhance the integration ability of global information in the decoding stage model.

- The Fast Normalized Fusion Method with trainable weights is used to efficiently fuse the corresponding three feature maps in encoding, bottleneck, and decoding, thus promoting information transmission and reducing the semantic gap between the encoder and decoder.

## 🔍 Dataset
All experiments are carried out on public data sets about polyps. You can download the dataset EndoScene from and create some folders like the figure below shows.
<p align="center"><img src='./Dataset.png'  width=300></p>
                      
                                  
