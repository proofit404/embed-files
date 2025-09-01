# embed-files

LLM embeddings for text files.

**[PyPI](https://pypi.org/project/embed-files) |
[Documentation](https://proofit404.github.io/embed-files) |
[Source Code](https://github.com/proofit404/embed-files) |
[Task Tracker](https://github.com/proofit404/embed-files/issues)**

```console
$ embed-files -m vendor/mxbai-embed-xsmall-v1.gguf -t '{}' dangerfile.ts
{"dangerfile.ts": [0.6499522924423218, 1.8278818130493164, -0.6607582569122314, -1.2485640048980713, -0.9449502229690552]}

$ embed-files -m vendor/nomic-embed-text-v1.5.gguf -t 'clustering: {}' dangerfile.ts
{"dangerfile.ts": [0.6499522924423218, 1.8278818130493164, -0.6607582569122314, -1.2485640048980713, -0.9449502229690552]}
```

## Questions

If you have any questions, feel free to create an issue in our
[Task Tracker](https://github.com/proofit404/embed-files/issues). We have the
[question label](https://github.com/proofit404/embed-files/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)
exactly for this purpose.

## Enterprise support

If you have an issue with any version of the library, you can apply for a paid
enterprise support contract. This will guarantee you that no breaking changes
will happen to you. No matter how old version you're using at the moment. All
necessary features and bug fixes will be backported in a way that serves your
needs.

Please contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you're
interested in it.

## License

`embed-files` library is offered under the two clause BSD license.
