#include <camera/camera_api.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    camera_handle_t camHandle;
    camera_buffer_t* buffer;

    // Open the first available camera
    if (camera_open(CAMERA_UNIT_FRONT, &camHandle) != CAMERA_EOK) {
        fprintf(stderr, "Failed to open camera\n");
        return 1;
    }

    // Start the viewfinder
    if (camera_start_viewfinder(camHandle, NULL, NULL, NULL) != CAMERA_EOK) {
        fprintf(stderr, "Failed to start viewfinder\n");
        camera_close(camHandle);
        return 1;
    }

    // Take one shot
    if (camera_take_photo(camHandle, NULL, &buffer) != CAMERA_EOK) {
        fprintf(stderr, "Failed to take photo\n");
        camera_stop_viewfinder(camHandle);
        camera_close(camHandle);
        return 1;
    }

    // Save image to file
    FILE* file = fopen("/tmp/image.jpg", "wb");
    if (!file) {
        fprintf(stderr, "Failed to open file for writing\n");
    } else {
        fwrite(buffer->framedesc.buf, 1, buffer->framedesc.size, file);
        fclose(file);
        printf("Saved photo to /tmp/image.jpg\n");
    }

    // Release buffer
    camera_release_buffer(camHandle, buffer);

    // Stop camera
    camera_stop_viewfinder(camHandle);
    camera_close(camHandle);

    return 0;
}