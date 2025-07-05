import os
import sys
import pyperclip


def copy_file_to_clipboard(file_path):
    try:
        with open(file_path, "r") as file:
            file_contents = file.read()
            pyperclip.copy(file_contents)
            print(f"Contents of '{file_path}' copied to clipboard.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_template_code_from_code(filename, generated):
    new_fn = "new_file.py"

    with open(filename, "r") as f:
        with open(new_fn, "w") as g:
            g.write(f"    def gen_{generated}(self):\n")

            add = {True: "=", False: "+="}
            line_no = 1
            for line in f:
                if '"' in line and "'" in line:
                    print(
                        f"Cannot construct template code for line {line_no} in {filename} due to "
                        "multiple quotation mark types. Please contruct manually: "
                        f"\n{line}"
                    )

                elif '"' in line:
                    g.write(
                        f"        self.{generated} {add[line_no == 1]} f'{line.rstrip()}\\n'\n"
                    )

                elif "'" in line:
                    g.write(
                        f'        self.{generated} {add[line_no == 1]} f"{line.rstrip()}\\n"\n'
                    )

                else:
                    g.write(
                        f"        self.{generated} {add[line_no == 1]} f'{line.rstrip()}\\n'\n"
                    )

                line_no += 1
            g.write(f"        self.{generated} {add[line_no == 1]} '\\n'\n\n")

    copy_file_to_clipboard(new_fn)


if __name__ == "__main__":
    """Usage:
        python <code_file> <generated_name> OR
        python inp.txt

    to run a series of code files with generated names all in an input file and
    concatenate them to a single template (2nd option)."""
    filename = sys.argv[1]

    if len(sys.argv) == 3:
        generated = sys.argv[2]
        generate_template_code_from_code(filename, generated)

    else:
        with open(filename, 'r') as f:
            template_file = "template_file.txt"
            for line in f:
                fname = line.split()[0]
                generated = line.split()[1]

                generate_template_code_from_code(fname, generated)

                os.system(f"cat new_file.py >> {template_file}")
                os.remove("new_file.py")


