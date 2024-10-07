# Proyecto-AN
# Numeric Methods CLI Application (Go)

This application allows you to run various numerical methods (e.g., Bisection, Newton's Method, Gaussian Elimination) using a simple command-line interface.

## Prerequisites

1. **Install Go**:  
   If you don't have Go installed, follow these steps:
   
   - Download and install Go from the official website: [https://golang.org/dl/](https://golang.org/dl/).
   - Follow the installation instructions for your operating system (Windows, macOS, Linux).

2. **Verify Go Installation**:  
   After installation, open a terminal (or command prompt) and run:

   ```bash
   go version
   ```

   This should display your Go version, indicating it’s installed correctly.

## Downloading and Running the Application

### 1. Clone or Download the Repository

If the source code is hosted in a repository (e.g., GitHub), clone the repository or download the source code. You can use the command below to clone it:

```bash
git clone https://github.com/unnamedpilot/Proyecto-AN.git
```

Alternatively, you can download the ZIP file containing the source code and extract it.

### 2. Navigate to the Project Directory

Use your terminal to navigate to the directory containing the source code files.

```bash
cd path_to_project_directory
```

### 3. Compile and Run the Program

Once inside the directory (go_modules), run the following command to build and execute the application:

```bash
go run .
```

Alternatively, you can build an executable file using:

```bash
go build -o go_modules
```

Then, run the executable:

```bash
./Numeric_Methods   # For Linux/macOS
Numeric_Methods.exe # For Windows
```

## Usage

Once the program is running, you will be prompted with a series of options. Select a method and provide the required inputs when prompted.

### Example

```
Choose the task:
1. Test a method
2. Evaluate a function

Enter the number of your choice: 1

Choose a mathematical method:
1. Búsquedas (Searches)
2. Bisección (Bisection)
...
8. Simple Gaussian Elimination
9. Gaussian Elimination with Partial Pivoting
10. Gaussian Elimination with Full Pivoting

Enter the number of your choice: 8
Enter the maximum number of iterations: 100
Enter the tolerance: 0.000001
Enter the size of the matrix (n x n): 3
Enter row 1 of matrix A (space-separated values): 2 1 -1
Enter row 2 of matrix A (space-separated values): -3 -1 2
Enter row 3 of matrix A (space-separated values): -2 1 2
Enter the vector b (space-separated values): 8 -11 -3

Result: 2.0000000000000000
```

## Troubleshooting

- If you encounter any issues, ensure that Go is installed correctly and that your environment variables (e.g., `GOPATH`, `GOROOT`) are properly configured.
- For more details on Go installation and configuration, refer to the official documentation: [https://golang.org/doc/install](https://golang.org/doc/install).
