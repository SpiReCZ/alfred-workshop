# Jak nasetupovat projekt?

Budete potřebovat Homebrew:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Poté nainstalujete pyenv, pyenv-virtualenv a portaudio:

```
brew install pyenv
brew install pyenv pyenv-virtualenv
brew install portaudio
```

Poté nainstalujete Python 3.12 a vytvoříte virtualenv:

```
pyenv install 3.12
pyenv virtualenv 3.12

#optionally nano .zshrc

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Poté nainstalujete závislosti:

```
pip install -r "requirements.txt"
```
