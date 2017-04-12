start_txt = 'start'
add_txt = 'add'
list_txt = 'list'
help_txt = 'help'
not_valid_email = 'not_valid_email'
email_already_added = 'email_already_added'
wait_password = 'wait_password'
error = 'error'
email_check_error = 'email_check_error'
email_successfully_added = 'email_successfully_added'

__en_texts = {
    start_txt : 'Hello! I can aggregate all your incoming emails and sent it to your Telegram. I use encryption and don\'t store your emails. So I\'m secure bot :)\nUse /add command to setup your email box. \nIf you have some questions or problems use /help command.',
    add_txt: 'Write your email address',
    list_txt: 'Here is your added emails:\n',
    help_txt: """
        Possible commands:
/add - add new email address
/list - show all your added email addresses
/help - show this message
/start  - show bot description

If you have problems with setting up your email make sure that:
1) two factor authorization is disabled on you email account
2) access by IMAP protocol is enabled

Email for questions: a.musin@outlook.com
        """,
    not_valid_email: 'Not valid email address. Try again',
    email_already_added: 'This email address is already added. Try again',
    wait_password: 'Write password. I use encryption to protect your data :)',
    error: 'Something goes wrong :( Use /help command',
    email_check_error: 'I can not connect to your email box. Check your email address and password or use /help command.',
    email_successfully_added: 'Email successfully added!'
    }


def get_text(command):
    return __en_texts[command]