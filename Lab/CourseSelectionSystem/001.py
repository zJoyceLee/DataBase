from gi.repository import Gtk, GLib
import socket
import sys
import threading

host=''
port=6666

def printSocketError(err):
    print('Socket error: code({}), {}'.format(err[0], err[1]))

def updateLabel(label, reply):
    original = label.get_text()
    label.set_text(original + '\n' + reply)
    return False

def updateRecvMessage(conn, label):
    while True:
        reply = conn.recv(4096)
        if len(reply) > 0:
            print(reply)
            GLib.idle_add(updateLabel, label, reply)

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Socket Sever")

        self.isSocketClosed = 1

        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error, e:
            printSocketError(e)

        grid = Gtk.Grid()
        self.add(grid)
        listenBtn = Gtk.Button(label="Listen")
        listenBtn.connect("clicked", self.on_listen_clicked)
        closeBtn = Gtk.Button(label="Close")
        closeBtn.connect("clicked", self.on_close_clicked)
        submitBtn = Gtk.Button(label="Submit")
        submitBtn.connect("clicked", self.on_submit_clicked)
        self.entry = Gtk.Entry()
        self.entry.set_text("Type here!")
        self.label = Gtk.Label('news: ')

        grid.add(listenBtn)
        grid.attach(closeBtn, 1, 0, 1, 1)
        grid.attach(submitBtn, 2, 0, 1, 1)
        grid.attach(self.entry, 0, 1, 3, 1)
        grid.attach(self.label, 0, 2, 3, 1)

    def close(self):
        if not self.isSocketClosed:
            print('close socket!')
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

    def __del__(self):
        self.close()

    def on_listen_clicked(self, widget):
        if not self.isSocketClosed:
            return

        try:
            self.sock.bind((host,port))
        except socket.error, e:
            printSocketError(e)
            self.close()
            Gtk.main_quit()
        self.label.set_text(self.label.get_text() + '\n'
                            + '$ Socket bind complete')

        self.sock.listen(10)
        self.label.set_text(self.label.get_text() + '\n'
                            + '$ Socket now listening')

        self.isSocketClosed = 0

        def client_thread(sock):
            while True:
                conn, addr = self.sock.accept()
                self.conn = conn
                GLib.idle_add(
                    lambda: self.label.set_text(
                        self.label.get_text() + '\n'
                        + '$ Connected with '
                        + str(addr[0])+ ':' + str(addr[1])))

                self.recvThread = threading.Thread(target=updateRecvMessage,
                                                   args=(self.conn, self.label))
                self.recvThread.daemon = True
                self.recvThread.start()

        thread = threading.Thread(target=client_thread,
                                  args=(self.sock,))
        thread.daemon = True # do not wait for the client_thread()'s return before exit
        thread.start()

    def on_close_clicked(self, widget):
        self.close()
        print('Goodbye')
        Gtk.main_quit()

    def on_submit_clicked(self, widget):
        if self.isSocketClosed:
            self.label.set_text(self.label.get_text() + '\n'
                                + '$ The connection is closed.')
        message=self.entry.get_text()
        try:
            self.conn.sendall(message)
        except socket.error, e:
            self.label.set_text(self.label.get_text() + '\n'
                                + '$ Send failed')
            printSocketError(e)
            self.close()
            Gtk.main_quit()
        print('Message send successfully')

win = MainWindow()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
