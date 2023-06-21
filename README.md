
# Ewondo Transcription Transform API (ETTA)

Transcription in Ewondo and in poorly endowed languages in general is a task that requires algorithmic processing in order to extract the various components: phonemes, syllables, tones, and so on.

This project therefore includes a syllabification algorithm as well as tone extraction algorithms for transcriptions written in the Ewondo language.

The project's resources are accessible via endpoints:

`/syll-word/{word}/` : Who returns the components of a word written in Ewondo.

`/syll-sent/{sentence}/` : Who returns the components for a sentence written in Ewondo

## Installation
The first step is to clone or download the project.

```
git clone <repo_url>
```
then move on to installing the various dependencies
```
cd ETTA/
pip install -r requirements.txt
```
## Starting
The restfull server architecture makes this library quick and easy to use. To start a local server, execute the command:

```
python main.py
```
By default, the server starts on port `2045`. The server can therefore be accessed at the address `127.0.0.1:2045` ou `localhost:2045`

You can specify the startup port (e.g. `3000`).
```
python main.py -p 3000
```

## Documentation
The server documentation is available from the url `localhost:2045/api/docs/` where you can test the various endpoints directly from a web interface.

## Licence

ETTA is released under the Apache License, version 2.0. The Apache license is a popular BSD-like license. ETTA can be redistributed for free, even for commercial purposes, although you can not take off the license headers (and under some circumstances, you may have to distribute a license document). Apache is not a viral license like the GPL, which forces you to release your modifications to the source code. Note that this project has no connection to the Apache Foundation, other than that we use the same license terms.




