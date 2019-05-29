from app import Application


def execute_from_terminal(args):

    if len(args) == 1:
        print("No parameters here! \nFor start this app use script\n\tpython startapp.py runserver")
        return -1
    else:
        command = args[1]
        if command == "runserver":
            port = 5555
            application = Application(port=port)
            #application.create_app()
            application.server.run(debug=True, port=port)
        else:
            print("Unsupported command! Use next commands:\n\t1. runserver\n\t2. createsuperuser")