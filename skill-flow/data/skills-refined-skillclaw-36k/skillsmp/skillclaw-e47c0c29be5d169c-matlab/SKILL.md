---
name: matlab
description: Use this skill when you need to perform numerical computing, data analysis, or scientific visualization using MATLAB or GNU Octave, especially for tasks involving matrix operations, linear algebra, and signal processing.
---

# MATLAB/Octave Scientific Computing

MATLAB is a numerical computing environment optimized for matrix operations and scientific computing. GNU Octave is a free, open-source alternative with high MATLAB compatibility.

## Quick Start

**Running MATLAB scripts:**
```bash
# MATLAB (commercial)
matlab -nodisplay -nosplash -r "run('script.m'); exit;"

# GNU Octave (free, open-source)
octave script.m
```

**Install GNU Octave:**
```bash
# macOS
brew install octave

# Ubuntu/Debian
sudo apt install octave

# Windows - download from https://octave.org/download
```

## Core Capabilities

### 1. Matrix Operations

MATLAB operates fundamentally on matrices and arrays:

```matlab
% Create matrices
A = [1 2 3; 4 5 6; 7 8 9];  % 3x3 matrix
v = 1:10;                     % Row vector 1 to 10
v = linspace(0, 1, 100);      % 100 points from 0 to 1

% Special matrices
I = eye(3);          % Identity matrix
Z = zeros(3, 4);     % 3x4 zero matrix
O = ones(2, 3);      % 2x3 ones matrix
R = rand(3, 3);      % Random uniform
N = randn(3, 3);     % Random normal

% Matrix operations
B = A';              % Transpose
C = A * B;           % Matrix multiplication
D = A .* B;          % Element-wise multiplication
E = A \ b;           % Solve linear system Ax = b
F = inv(A);          % Matrix inverse
```

### 2. Linear Algebra

```matlab
% Eigenvalues and eigenvectors
[V, D] = eig(A);     % V: eigenvectors, D: diagonal eigenvalues

% Singular value decomposition
[U, S, V] = svd(A);

% Matrix decompositions
[L, U] = lu(A);      % LU decomposition
[Q, R] = qr(A);      % QR decomposition
```

### 3. Additional Functions

MATLAB also supports various functions for signal processing, image processing, optimization, and statistics. Use this skill to get help with MATLAB syntax, functions, or converting between MATLAB and Python code.