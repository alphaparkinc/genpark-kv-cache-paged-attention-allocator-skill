import math
from typing import List, Dict, Any

class PagedKVCacheAllocator:
    def __init__(self, block_size: int = 16, num_blocks: int = 128):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.free_blocks = list(range(num_blocks))
        self.seq_block_map: Dict[str, List[int]] = {}

    def allocate(self, seq_id: str, num_tokens: int) -> Dict[str, Any]:
        needed = math.ceil(num_tokens / self.block_size)
        if len(self.free_blocks) < needed:
            return {"error": "Out of memory", "available": len(self.free_blocks), "needed": needed}
        allocated = [self.free_blocks.pop(0) for _ in range(needed)]
        self.seq_block_map[seq_id] = allocated
        frag = (needed * self.block_size - num_tokens) / (needed * self.block_size)
        return {
            "seq_id": seq_id,
            "allocated_blocks": allocated,
            "tokens_stored": num_tokens,
            "internal_fragmentation_ratio": round(frag, 4),
            "free_blocks_remaining": len(self.free_blocks)
        }

    def free(self, seq_id: str) -> Dict[str, Any]:
        if seq_id not in self.seq_block_map:
            return {"error": "Seq not found"}
        blocks = self.seq_block_map.pop(seq_id)
        self.free_blocks.extend(blocks)
        return {"seq_id": seq_id, "freed_blocks": blocks, "free_blocks_remaining": len(self.free_blocks)}

    def benchmark_allocation(self) -> Dict[str, Any]:
        a1 = self.allocate("seq-01", 45)
        a2 = self.allocate("seq-02", 70)
        return {"alloc_1": a1, "alloc_2": a2, "remaining_blocks": len(self.free_blocks)}
