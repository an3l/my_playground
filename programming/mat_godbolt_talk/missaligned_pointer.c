int8_t *buffer = malloc(64);
int32_t *pointer = (int32_t *)(buffer + 1);
*pointer = 42; // Error: misaligned integer pointer assignment

//https://developer.apple.com/documentation/code_diagnostics/undefined_behavior_sanitizer/misaligned_pointer
