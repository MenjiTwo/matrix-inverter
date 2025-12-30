# Matrix Inverter

A cross-platform GUI application for inverting matrices, built with Python and tkinter.

## 📥 Download

**[Download the latest release](../../releases/latest)** - Pre-built executables available for:
- 🪟 **Windows** - `matrix-inverter-windows.exe`
- 🐧 **Linux** - `matrix-inverter-linux`
- 🍎 **macOS** - `matrix-inverter-macos`

Just download the file for your operating system and run it - no installation required!

> **Note for Linux/macOS users:** You may need to make the file executable first:
> ```bash
> chmod +x matrix-inverter-linux  # or matrix-inverter-macos
> ./matrix-inverter-linux
> ```

---

## Features

- **Intuitive GUI**: Easy-to-use graphical interface for entering matrices
- **Variable Matrix Size**: Support for 2x2 up to 10x10 matrices
- **Step-by-Step Solutions**: Shows elementary row operations used
- **LaTeX Format View**: Toggle LaTeX-style matrix display
- **Real-time Validation**: Input validation with helpful error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## For Developers

### Requirements

- Python 3.8 or higher
- NumPy
- tkinter (usually included with Python)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MenjiTwo/matrix-inverter.git
   cd matrix_inverter
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the application:

```bash
python matrix_inverter.py
```

### Building Executables Locally

To build an executable on your machine:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "matrix-inverter" matrix_inverter.py
```

The executable will be in the `dist/` folder.

## How to Use

1. **Select Matrix Size**: Use the spinbox to choose the matrix dimension (NxN)
2. **Enter Values**: Input your matrix values in the left grid
3. **Calculate**: Click "Calculate Inverse" to compute the inverse
4. **View Results**: The inverse matrix appears in the right grid
5. **View Steps**: See the elementary row operations in the table below

## Mathematical Background

A matrix A is invertible if there exists a matrix A⁻¹ such that:

```
A × A⁻¹ = A⁻¹ × A = I
```

Where I is the identity matrix.

**Note**: A matrix is only invertible if its determinant is non-zero.

## License

MIT License - Feel free to use and modify as needed.
