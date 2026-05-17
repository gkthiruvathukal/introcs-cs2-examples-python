PYTHON = .venv/bin/python
PYTEST  = .venv/bin/pytest

# Convenience short aliases
RUN_ALIASES  = run-bst run-deque run-dict run-dll run-graph run-heap \
               run-list run-networkx run-queue run-set run-sll run-stack run-stack-tui \
               run-queue-tui run-deque-tui run-list-tui run-sll-tui run-dll-tui run-trie
TEST_ALIASES = test-bst test-deque test-dict test-dll test-graph test-heap \
               test-list test-networkx test-queue test-set test-sll test-stack test-stack-tui \
               test-queue-tui test-deque-tui test-list-tui test-sll-tui test-dll-tui test-trie

.PHONY: install test $(RUN_ALIASES) $(TEST_ALIASES)

# Create the virtual environment
.venv:
	python3 -m venv .venv

# Install dependencies into the venv
install: .venv
	$(PYTHON) -m pip install -r requirements.txt

# Run all tests
test:
	$(PYTEST) tests/

# Short aliases
run-bst:     run-binary_search_tree_demo
run-deque:   run-deque_demo
run-dict:    run-dictionary_demo
run-dll:     run-doubly_linked_list
run-graph:   run-graph_demo
run-heap:    run-heap_demo
run-list:    run-list_demo
run-networkx: run-networkx_graph_demo
run-queue:   run-queue_demo
run-queue-tui: run-queue_demo_tui
run-set:     run-set_demo
run-sll:     run-singly_linked_list
run-sll-tui: run-singly_linked_list_tui
run-stack:     run-stack_demo
run-stack-tui: run-stack_demo_tui
run-deque-tui: run-deque_demo_tui
run-list-tui: run-list_demo_tui
run-dll-tui: run-doubly_linked_list_tui
run-trie:    run-trie_demo

test-bst:     test-binary_search_tree_demo
test-deque:   test-deque_demo
test-dict:    test-dictionary_demo
test-dll:     test-doubly_linked_list
test-graph:   test-graph_demo
test-heap:    test-heap_demo
test-list:    test-list_demo
test-networkx: test-networkx_graph_demo
test-queue:   test-queue_demo
test-queue-tui: test-queue_demo_tui
test-set:     test-set_demo
test-sll:     test-singly_linked_list
test-sll-tui: test-singly_linked_list_tui
test-stack:   test-stack_demo
test-stack-tui: test-stack_demo_tui
test-deque-tui: test-deque_demo_tui
test-list-tui: test-list_demo_tui
test-dll-tui: test-doubly_linked_list_tui
test-trie:    test-trie_demo

# Run a single demo module:  make run-<name>
#   Note: demo files contain only class definitions (no __main__),
#   so these targets verify clean import but produce no output.
#
#   Valid names:
#     binary_search_tree_demo   deque_demo         dictionary_demo
#     doubly_linked_list        graph_demo         heap_demo
#     list_demo                 networkx_graph_demo  queue_demo
#     queue_demo_tui            deque_demo_tui     list_demo_tui
#     singly_linked_list        singly_linked_list_tui
#     doubly_linked_list_tui    set_demo           stack_demo
#     stack_demo_tui            trie_demo
run-%:
	$(PYTHON) -m data_structures.$*

# Run a single test module:  make test-<name>
#
#   Valid names (same list as above):
#     binary_search_tree_demo   deque_demo         dictionary_demo
#     doubly_linked_list        graph_demo         heap_demo
#     list_demo                 networkx_graph_demo  queue_demo
#     queue_demo_tui            deque_demo_tui     list_demo_tui
#     singly_linked_list        singly_linked_list_tui
#     doubly_linked_list_tui    set_demo           stack_demo
#     stack_demo_tui            trie_demo
test-%:
	$(PYTEST) tests/test_$*.py -v
