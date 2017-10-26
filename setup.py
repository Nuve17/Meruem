import argparse, sys
import send_api_Slack
import send_email
import argparse

def main():

    parser = argparse.ArgumentParser(description='ESGI Planning Automatic Guetto Guetter.')
    parser.add_argument('-w', '--web',help='Start the web server for printing planning', action='store_true')
    parser.add_argument('-s', '--slack', help='Send the planning on the slack team', action='store_true')
    parser.add_argument('-m', '--mail', help='Send the calendar by mail ', action='store_true')
    parser.add_argument('-f', '--file', help='Path to file contain email address one pair line')
    args = parser.parse_args()


    print args.file is not None
    print args.mail
    if len(sys.argv)==1:
        print parser.print_help()
    else:
        if args.web:
            print "Starting web server"
            import app_web_server
            app_web_server.main()
        if args.slack:
            send_api_Slack.main()
        if args.mail==True and args.file==False:
            print "No file contain email address are specify"
        elif args.mail==True and args.file is not None:
            print args.file
            send_email.main(args.file)

if __name__ == '__main__':
    main()
