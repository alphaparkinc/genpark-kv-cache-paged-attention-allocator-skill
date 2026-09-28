from client import PagedKVCacheAllocator

def run_example():
    print("=== GenPark Paged KV-Cache Allocator Example ===")
    mgr = PagedKVCacheAllocator(block_size=16, num_blocks=64)
    print("Allocate:", mgr.allocate("user-1", 50))
    print("Free:", mgr.free("user-1"))

if __name__ == "__main__":
    run_example()
