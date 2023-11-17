# Tensors

A tensor is a mathematical object that generalizes the concepts of scalars, vectors, and matrices to higher dimensions. 
It's a key concept in fields such as physics and engineering, particularly in the study of linear algebra, continuum 
mechanics, and tensor calculus. 

### Here's a breakdown of what a tensor is:

1. **Scalars**: A scalar is a single number, representing a quantity like temperature or mass. In tensor terms, a scalar
   is a tensor of rank 0. 
   <br/><br/>

2. **Vectors**: A vector is an array of numbers, representing quantities that have both magnitude and direction, like 
   velocity or force. In tensor language, a vector is a tensor of rank 1.
   <br /> <br />

4. **Matrices**: A matrix is a 2-dimensional array of numbers, often used to represent linear transformations or 
   relationships between vectors. In the world of tensors, a matrix is a tensor of rank 2.
   <br /><br />
    
4. **Higher-Dimensional Tensors**: Tensors can extend beyond matrices to higher dimensions. For example, a 3-dimensional 
   tensor could be thought of as a cube of numbers, and a 4-dimensional tensor as a hypercube of numbers. These are 
   used in more complex scenarios, like describing the stress or strain in a 3D material, or in advanced data structures
   in machine learning.

Tensors are defined by two key properties: 
1. Their rank (or order), which is the number of dimensions in the tensor
2. Their shape, which is the size of each dimension. For example, a 2x2 matrix is a rank-2 tensor with a shape of 2x2.

In modern usage, especially in machine learning, the term "tensor" is often used to describe multidimensional arrays of
numbers in general, regardless of their rank. Libraries like [`TensorFlow`](https://www.tensorflow.org/) and 
[`PyTorch`](https://pytorch.org/), used for deep learning, use tensors as their fundamental data structure.