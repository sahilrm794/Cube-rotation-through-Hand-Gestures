# **HandControlledCube**

Welcome to the HandControlledCube repository! This project features a basic 3D cube visualization implemented with Pygame. The rotation of the cube can be controlled through hand gestures detected by a separate module.

### Files Included:

1. **cube.py**: This script creates a Pygame window and displays a rotating 3D cube. The rotation of the cube can be adjusted using keyboard commands.

2. **CordReader1.py**: This script is designed to capture hand gesture data from a sensor or file (though these are not provided) and update the cube's rotation accordingly. It seems to function similarly to `cube.py`.

### Steps to Run:

1. Clone the repository to your local system:

    ```
    git clone https://github.com/your-username/HandControlledCube.git
    ```

2. Install the required dependencies:

    ```
    pip install pygame
    ```

3. Execute either the `Cube.py` or `CordReader1.py` script using Python:

    ```
    python Cube.py
    ```

    or

    ```
    python CordReader1.py
    ```

4. Control the cube’s rotation using the following keyboard inputs: (`a`, `d`, `w`, `s`, `q`, `e`, `r`).

### Additional Information:

- Both scripts contain a main loop that manages the cube's rotation and processes user input.

- To modify the cube's rotation angles, simply adjust the `angle_x`, `angle_y`, and `angle_z` variables.

- Although the `angle.json` file seems intended for storing rotation angles, it is not fully utilized in the current implementation.

- Feel free to explore the code and make any modifications as needed.

### Contributors:

- [Sahil Rajesh Mustilwar](https://github.com/sahilrm794)

### License:

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Acknowledgments:

- This project was inspired by the idea of creating interactive 3D visualizations using Python and Pygame.

- A special thank you to the Pygame community for the helpful resources and tutorials.
