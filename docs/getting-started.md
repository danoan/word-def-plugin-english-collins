# Getting started with word-def Plugin English Collins

Plugin to word-def package that connects with the English Collins dictionary API.

## Installation

```bash
$ pipx install word-def-plugin-english-collins
```

## Features

- Get word definition.
- Get part-of-speech tags of a word.

## Examples

```{admonition} word-def
You need to have the [word-def](https://github.com/danoan/word-def) package installed.
```


```bash
$ word-def --plugin-configuration-filepath plugin-config.toml get-definition joy eng

1. a deep feeling or condition of happiness or contentment
2. something causing such a feeling; a source of happiness
3. an outward show of pleasure or delight; rejoicing
4. success; satisfaction
5. to make joyful; gladden
```

```{admonition} Plugin configuration
   The [word-def documentation](https://danoan.github.io/word-def/how-to/setup-a-plugin.html)
   has more information about how to setup the plugin configuration file.
```
## Plugin parameters

To configure the plugin, create the `plugin-config.toml` file similar to the one below:

```toml
entrypoint="COLLINS API URL"
secret_key="PERSONAL SECRET KEY"
```

## Contributing

Please reference to our [contribution](http://danoan.github.io/word-def-plugin-english-collins/contributing) and [code-of-conduct](http://danoan.github.io/word-def-plugin-english-collins/code-of-conduct) guidelines.
