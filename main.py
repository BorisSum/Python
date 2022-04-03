from Stack import Stack


def main():
    stack = Stack.create_stack('New Stack')
    print(stack.stack_name)
    stack.stack_name = 'Super New Stack'
    print(stack.stack_name)


if __name__ == "__main__":
    main()
