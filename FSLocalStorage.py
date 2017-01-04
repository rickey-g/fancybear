import os
import random

os.umask(0000)


class FSLocalStorageException(BaseException):
    pass


class FSLocalStorageCriticalException(BaseException):
    pass


class FSLocalStorage(object):
    def __init__(self, _root_path=None, _data_folder='data', _from_folder='1', _to_folder='2', status_file='.last'):
        if not _root_path:
            self.root_path = os.path.dirname(os.path.abspath(__file__))
        else:
            self.root_path = _root_path
        if not os.path.exists(self.root_path):
            raise FSLocalStorageCriticalException("Root path is invalid!")
        #
        self.data_dir = os.path.join(self.root_path, _data_folder)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        #
        self.from_agent_folder = _from_folder
        self.to_agent_folder = _to_folder
        self.status_file = status_file

    def init_storage_for_agent(self, agent_id):
        agent_folder = os.path.join(self.data_dir, str(agent_id))
        if not os.path.exists(agent_folder):
            print "# FSLocalStorage: NEW ", str(agent_id)
            os.mkdir(agent_folder)
            os.mkdir(os.path.join(agent_folder, self.to_agent_folder))
            os.mkdir(os.path.join(agent_folder, self.from_agent_folder))
        else:
            to_folder = os.path.join(agent_folder, self.to_agent_folder)
            if not os.path.exists(to_folder):
                os.mkdir(to_folder)

            from_folder = os.path.join(agent_folder, self.from_agent_folder)
            if not os.path.exists(from_folder):
                os.mkdir(from_folder)
        return agent_folder

    def get_oldest_filename(self, agent_id, stream):
        agent_folder = os.path.join(self.init_storage_for_agent(agent_id), stream)
        files = filter(lambda x: os.path.isfile(os.path.join(agent_folder, x)), os.listdir(unicode(agent_folder)))
        if files:
            files = sorted(files, key=lambda x: os.stat(os.path.join(agent_folder, x)).st_ctime)
            return os.path.join(agent_folder, files[0])
        else:
            return None

    def get_filename_by_mark(self, agent_id, stream, mark):
        agent_folder = os.path.join(self.init_storage_for_agent(agent_id), stream)
        filename = os.path.join(agent_folder, mark)
        if os.path.exists(filename):
            return filename
        else:
            return None

    def read_last_data(self, agent_id, stream):
        mark = ''
        res_body = ''
        fname = self.get_oldest_filename(agent_id, stream)
        if fname and os.path.isfile(fname):
            # read oldest
            f = open(fname, 'rb')
            res_body = f.read()
            f.close()
            mark = os.path.split(fname)[1]
        return mark, res_body

    def remove_data(self, agent_id, stream, mark):
        mark = mark.replace('/', '').replace('\\', '').replace("..", '')
        fname = self.get_filename_by_mark(agent_id, stream, mark)
        if fname and os.path.isfile(fname):
            os.unlink(fname)

    def write_data(self, agent_id, stream, data):
        agent_folder = os.path.join(self.init_storage_for_agent(agent_id), stream)
        fname = os.path.join(agent_folder, str(random.randint(0, 0xffffffff)))
        f = open(fname, 'wb')
        f.write(data)
        f.close()

    # Agent communication
    def save_data_from_agent(self, agent_id, data):
        self.write_data(agent_id, self.from_agent_folder, data)

    def get_data_for_agent(self, agent_id):
        return self.read_last_data(agent_id, self.to_agent_folder)

    def data_for_agent_accepted(self, agent_id, mark):
        return self.remove_data(agent_id, self.to_agent_folder, mark)

    def save_status_info_for_agent(self, agent_id, info):
        agent_folder = self.init_storage_for_agent(agent_id)
        status_file = os.path.join(agent_folder, self.status_file)
        f = open(status_file, "w")
        f.write(info)
        f.close()

    def get_status_info_for_agent(self, agent_id):
        agent_folder = self.init_storage_for_agent(agent_id)
        status_file = os.path.join(agent_folder, self.status_file)
        info = ''
        try:
            f = open(status_file, "r")
            info = f.read()
            f.close()
        except:
            print "# FSLocalStorage: Cannot to open and read status file for %d !" % agent_id
        return info

    # CC communication
    def get_agents_list(self):
        aids = map(lambda x: int(x), filter(lambda x: x.isdigit(), os.listdir(self.data_dir)))
        return aids

    def save_data_for_agent(self, agent_id, data):
        self.write_data(agent_id, self.to_agent_folder, data)

    def get_data_from_agent(self, agent_id):
        return self.read_last_data(agent_id, self.from_agent_folder)

    def data_from_agent_accepted(self, agent_id, mark):
        return self.remove_data(agent_id, self.from_agent_folder, mark)
