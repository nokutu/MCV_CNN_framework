# ResNet

Network depth is a crucial factor for the performance of a model, but just adding more layers leads to the problem of vanishing gradients. This problem has been addressed with normalized initialization and intermediate normalization layers. But there is also the problem of degradation: as the depth increases, accuracy gets saturated and starts degrading rapidly. ResNets address the degradation problem by introducing residual connections.

Layers are reformulated as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. The reformulation is motivated by the observation that if more layers are added to a given model, then the new model should have a training error no greater than the original model, since the new layers can be identity mappings. However, the degradation problem suggests that solvers might not able to do this. Residual connections improve optimization by helping solvers achieve these identity mappings. Authors hypothesize that it should be easier for the solver to find the right mapping with reference to an identity mapping, than to learn the function from scratch.

The new formulation adds "shortcut connections", but does not introduce extra parameters nor computational complexity, which is quite convenient. Shortcut connections usually skip two or three layers (or even more), but they do not present improvements for a single layer. Skipped layers can be either fully-connected or convolutional layers.