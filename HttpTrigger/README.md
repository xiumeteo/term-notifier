This is a side project to notify me when a long-running command terminates.
It uses: 
- Twilio
- Azure Functions
- Python
- Oh my zsh 
    - And the auto-notify plugin.

Installation
===========

First make sure you have Zsh and the [auto-notify](https://github.com/MichaelAquilina/zsh-auto-notify) plugin. And of course, you have Python 3+ installed.

- Clone the code.
- Then rename the `test.env` file using your own parameters.
- Open your `.zshrc` and define an env path called `TERM_NOTIFIER` which should point to the cloned folder.
- Open the file `auto-notify.plugin.zsh` on the customs/plugins folder of zsh
- Define at the top a new var:
```zsh
export TERM_NOTIFIER_THRESHOLD=60
```
- Add this snippet under the `_auto_notify_send` function
```zsh
if [[ $elapsed -gt $TERM_NOTIFIER_THRESHOLD ]]; then
    "$(python3 $TERM_NOTIFIER/sender.py "$AUTO_COMMAND" "$elapsed" "$exit_code" )"
fi
```

- Finally follow the steps [to create a valid OTP](https://pyotp.readthedocs.io/en/latest/)

Tips
===
It is a good idea to create a virtual env in the folder of installation.
