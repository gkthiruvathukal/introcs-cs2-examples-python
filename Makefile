PYTHON = .venv/bin/python
PYTEST  = .venv/bin/pytest

# Convenience short aliases
RUN_ALIASES  = run-bst run-deque run-dict run-dll run-graph run-heap \
               run-list run-networkx run-queue run-set run-sll run-stack run-trie
TEST_ALIASES = test-bst test-deque test-dict test-dll test-graph test-heap \
               test-list test-networkx test-queue test-set test-sll test-stack test-stack-app \
               test-queue-app test-deque-app test-list-app test-sll-app test-dll-app test-trie

.PHONY: install test $(RUN_ALIASES) $(TEST_ALIASES) \
        run-stack-app run-queue-app run-deque-app run-list-app run-sll-app run-dll-app

# Create the virtual environment
.venv:
	python3 -m venv .venv

# Install dependencies into the venv
install: .venv
	$(PYTHON) -m pip install -r requirements.txt

# Run all tests
test:
	$(PYTEST) tests/

# Short aliases — non-TUI demos
run-bst:     run-binary_search_tree_demo
run-deque:   run-deque_demo
run-dict:    run-dictionary_demo
run-dll:     run-doubly_linked_list
run-graph:   run-graph_demo
run-heap:    run-heap_demo
run-list:    run-list_demo
run-networkx: run-networkx_graph_demo
run-queue:   run-queue_demo
run-set:     run-set_demo
run-sll:     run-singly_linked_list
run-stack:   run-stack_demo
run-trie:    run-trie_demo

# App run targets (data_structures.tui.*)
run-stack-app:
	$(PYTHON) -m data_structures.tui.stack_app

run-queue-app:
	$(PYTHON) -m data_structures.tui.queue_app

run-deque-app:
	$(PYTHON) -m data_structures.tui.deque_app

run-list-app:
	$(PYTHON) -m data_structures.tui.list_app

run-sll-app:
	$(PYTHON) -m data_structures.tui.singly_linked_list_app

run-dll-app:
	$(PYTHON) -m data_structures.tui.doubly_linked_list_app

# Test aliases
test-bst:     test-binary_search_tree_demo
test-deque:   test-deque_demo
test-dict:    test-dictionary_demo
test-dll:     test-doubly_linked_list
test-graph:   test-graph_demo
test-heap:    test-heap_demo
test-list:    test-list_demo
test-networkx: test-networkx_graph_demo
test-queue:   test-queue_demo
test-queue-app: test-queue_app
test-set:     test-set_demo
test-sll:     test-singly_linked_list
test-sll-app: test-singly_linked_list_app
test-stack:   test-stack_demo
test-stack-app: test-stack_app
test-deque-app: test-deque_app
test-list-app: test-list_app
test-dll-app: test-doubly_linked_list_app
test-trie:    test-trie_demo

# Run a single non-TUI demo module:  make run-<name>
#   Note: demo files contain only class definitions (no __main__),
#   so these targets verify clean import but produce no output.
#
#   Valid names:
#     binary_search_tree_demo   deque_demo         dictionary_demo
#     doubly_linked_list        graph_demo         heap_demo
#     list_demo                 networkx_graph_demo  queue_demo
#     set_demo                  singly_linked_list   stack_demo
#     trie_demo
run-%:
	$(PYTHON) -m data_structures.$*

# Run a single test module:  make test-<name>
#
#   Valid names (same list as above, plus app variants):
#     binary_search_tree_demo   deque_demo         dictionary_demo
#     doubly_linked_list        graph_demo         heap_demo
#     list_demo                 networkx_graph_demo  queue_demo
#     queue_app                 deque_app          list_app
#     singly_linked_list        singly_linked_list_app
#     doubly_linked_list_app    set_demo           stack_demo
#     stack_app                 trie_demo
test-%:
	$(PYTEST) tests/test_$*.py -v
