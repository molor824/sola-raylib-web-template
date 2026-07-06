# Rust raylib web template using `sola-raylib` library.

## Requirements

* Raylib's own requirements
* `emcc` compiler
* Python

## Setup

Simply fork this repository, rename your project in `Cargo.toml` and it should work as it is

## Limitations

* Building to web without `--release` flag throws error.
* `link-arg=-sALLOW_MEMORY_GROWTH=1` is causing WebGL functions to throw TypeError. The only way I could fix it was with fixed initial memory `link-arg=-sINITIAL_MEMORY=64MB`, meaning if you're having out of memory issues, consider changing it in `.cargo/config.toml`.
