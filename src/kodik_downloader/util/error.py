errors = []

def log_error(text, errors_out):
    errors.append(text)
    if errors_out != None:
        errors_out.write(text + "\n")
