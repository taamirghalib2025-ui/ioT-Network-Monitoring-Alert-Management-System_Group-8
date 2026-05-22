from typing import Optional, List
from dataclasses import dataclass

# --- 1. DATA CLASSES ---
@dataclass
class Alert:
    alert_id: int
    device_id: str
    tipe: int  # 1=CRITICAL, 2=WARNING, 3=INFO
    pesan: str
    timestamp: float

# --- 2. NODE DASAR ---
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None

# --- 3. PRIORITY QUEUE (Untuk Alert Masuk) ---
class AlertPriorityQueue:
    """Linked List terurut tipe ASC (CRITICAL=1 di depan)."""
    
    def __init__(self):
        self.head: Optional[LLNode] = None
        self.size: int = 0

    def enqueue(self, alert: Alert) -> None:
        """Big-O: O(n) insertion berdasarkan prioritas."""
        new_node = LLNode(alert)
        
        # Jika antrean kosong ATAU prioritas alert baru lebih tinggi
        if self.head is None or alert.tipe < self.head.data.tipe:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            # Cari posisi yang tepat di tengah atau akhir antrean
            while current.next is not None and current.next.data.tipe <= alert.tipe:
                current = current.next
            
            new_node.next = current.next
            current.next = new_node
            
        self.size += 1

    def dequeue(self) -> Optional[Alert]:
        """Big-O: O(1)."""
        if self.head is None:
            return None
        
        popped_alert = self.head.data
        self.head = self.head.next
        self.size -= 1
        return popped_alert

    def __len__(self): 
        return self.size

# --- 4. STACK (Untuk History per Device) ---
class AlertStack:
    def __init__(self, kapasitas=20):
        self.top: Optional[LLNode] = None
        self.size = 0
        self.kapasitas = kapasitas

    def push(self, alert: Alert) -> None:
        """Big-O: O(1) untuk push."""
        new_node = LLNode(alert)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        
        # Jika kapasitas penuh, hapus elemen paling bawah (oldest)
        if self.size > self.kapasitas:
            current = self.top
            while current.next and current.next.next:
                current = current.next
            current.next = None
            self.size -= 1

    def pop(self) -> Optional[Alert]:
        """Big-O: O(1)."""
        if self.top is None:
            return None
            
        popped_alert = self.top.data
        self.top = self.top.next
        self.size -= 1
        return popped_alert

    def to_list(self) -> List[Alert]:
        alert_list = []
        current = self.top
        while current:
            alert_list.append(current.data)
            current = current.next
        return alert_list