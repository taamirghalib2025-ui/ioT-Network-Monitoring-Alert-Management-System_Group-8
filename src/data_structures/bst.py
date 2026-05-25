
"""
BST Device Registry
Kunci: device_id
Node menyimpan: id, tipe (SENSOR/GATEWAY/SERVER), status (ONLINE/OFFLINE), last_reading
Big-O: O(log n) rata-rata
"""

class DeviceNode:
    def __init__(self, device_id, tipe, status="ONLINE", last_reading=0.0):
        self.device_id    = device_id
        self.tipe         = tipe          # SENSOR / GATEWAY / SERVER
        self.status       = status        # ONLINE / OFFLINE
        self.last_reading = last_reading
        self.left         = None
        self.right        = None

    def __repr__(self):
        return f"Device(id={self.device_id}, tipe={self.tipe}, status={self.status}, reading={self.last_reading})"


class BSTDeviceRegistry:
    def __init__(self):
        self.root = None

    # INSERT — O(log n)
    def insert(self, device_id, tipe, status="ONLINE", last_reading=0.0):
        node = DeviceNode(device_id, tipe, status, last_reading)
        if self.root is None:
            self.root = node
            return
        cur = self.root
        while True:
            if device_id < cur.device_id:
                if cur.left is None:  cur.left = node; break
                cur = cur.left
            elif device_id > cur.device_id:
                if cur.right is None: cur.right = node; break
                cur = cur.right
            else:
                raise ValueError(f"device_id {device_id} sudah ada.")

    # SEARCH — O(log n)
    def search(self, device_id):
        cur = self.root
        while cur:
            if device_id == cur.device_id: return cur
            cur = cur.left if device_id < cur.device_id else cur.right
        return None

    # UPDATE STATUS — O(log n)
    def update_status(self, device_id, new_status, last_reading=None):
        node = self.search(device_id)
        if node is None:
            return False
        node.status = new_status
        if last_reading is not None:
            node.last_reading = last_reading
        return True

    # INORDER — O(n), daftar terurut by id
    def inorder(self):
        result = []
        def _traverse(node):
            if node:
                _traverse(node.left)
                result.append(node)
                _traverse(node.right)
        _traverse(self.root)
        return result