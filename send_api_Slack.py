# coding: utf-8

from slackclient import SlackClient
import pdf_getter
import os, io


def send_message(msg, channel, attachment=None):
    '''
    Plain send text method
    '''
    try:
        res = slack_client.api_call("chat.postMessage", channel=channel, text=msg, attachments=attachment, as_user=True)
        if not res.get('ok'):
            print res
            print 'error:', res.get('error')
    except:
        print('send_message failed')

def upload_file( filename, content, channel):
    '''
    upload a long text as a file
    '''
    ret = slack_client.api_call("files.upload", filename=filename, channels=channel, file= open(filename, 'rb'), content="Salut")

    if not 'ok' in ret or not ret['ok']:
        # error
        print ret
        print 'fileUpload failed', ret['error']
def main():
    global slack_client
    slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))
    channel='#planning'

    send_message("Hello, voici votre planning:", channel)
    upload_file(pdf_getter.main(), 'Hello', channel)
    send_message("Bonne semaine, Meruem-sama", channel)

if __name__ == '__main__':
    main()
