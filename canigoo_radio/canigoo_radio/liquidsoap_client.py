# This file is a part of the Canigoo radio project
#
#    Copyright (C) 2017 Franck Bret <franckbret@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import socket
from logging import getLogger


logger = getLogger(__name__)


class LiquidsoapClient:
    """ A class to interact with Liquisoap through linux socket
    """

    def send(self, cmd):

        data = None

        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect("/tmp/liquidsoap.sock")
            if type(cmd) != bytes:
                cmd = str.encode(cmd + "\n")
            logger.info("sending : {!r}".format(cmd))
            sock.sendall(cmd)
            data = sock.recv(4096)
            logger.info("received : {!r}".format(data))
        except:
            error = dict(error=("liquidsoap socket error", "socket communication failed"))
            logger.warn("socket error : {!r}".format(error))
            return error
        finally:
            logger.info("closing socket")
            sock.close()
            logger.info("socket closed")

        if not data:
            return dict()
        else:
            data = str(
                data.split(b"\r\nEND")[0], encoding='utf-8').lstrip().rstrip()
            data_dict = dict()
            if "\r\n" in data:
                data = data.split("\r\n")
                for line in data:
                    if " : " in line:
                        k, v = line.split(" : ")
                        data_dict[k] = v
            return data_dict or data

    @staticmethod
    def parse_metadatas(metadatas):
        try:
            return dict([(el[0], el[1][1:-1]) for el in [el.split('=') for el in metadatas.split('\n')]])
        except IndexError:
            retour = {}
            for el in metadatas.split('\n'):
                if '=' in el:
                    sp = el.split('=')
                    retour[sp[0]] = "=".join(el[1:])[1:-1]
            return retour
