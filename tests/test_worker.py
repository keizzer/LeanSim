from leansim import Worker


def test_worker_works():
    w = Worker()
    w.todo = 1
    assert w.done == 0
    w.work()
    assert w.done == 1
    assert w.todo == 0


def test_worker_works_slowly_when_long_task_duration():
    w = Worker(task_duration=2)
    w.todo = 1
    assert w.todo == 1
    w.work()
    assert w.todo == 0
    assert len(w.doing) == 1
    assert w.done == 0
    w.work()
    assert len(w.doing) == 0
    assert w.done == 1


def test_worker_works_slowly_when_long_task_duration2():
    w = Worker(task_duration=2)
    w.todo = 2
    assert w.todo == 2
    w.work()
    assert w.todo == 1
    assert len(w.doing) == 1
    assert w.done == 0
    w.work()
    assert w.todo == 1
    assert len(w.doing) == 0
    assert w.done == 1


def test_worker_can_multitask():
    w = Worker(capacity=2)
    w.todo = 4
    w.work()
    assert w.todo == 2
    assert len(w.doing) == 0
    assert w.done == 2

    w = Worker(capacity=2, task_duration=2)
    w.todo = 4
    w.work()
    assert w.todo == 2
    assert len(w.doing) == 2
    assert w.done == 0
    w.work()
    assert w.todo == 2
    assert len(w.doing) == 0
    assert w.done == 2


def test_worker_can_pass_on_work():
    w1, w2 = Worker(), Worker()
    w1.target = w2
    w1.todo = 2
    assert w1.todo == 2 and w1.done == 0
    assert w2.todo == 0 and w2.done == 0
    w1.work()
    assert w1.todo == 1 and w1.done == 1
    assert w2.todo == 0 and w2.done == 0
    w1.push()
    assert w2.todo == 1 and w2.done == 0


def test_worker_passes_on_all_work_in_batch():
    for batch_size in range(1, 10):
        w1, w2 = Worker(batch_size=batch_size), Worker()
        w1.target = w2
        w1.done = batch_size + 1
        w1.push()
        assert w1.done == 1 and w2.todo == batch_size


def test_worker_does_not_accept_too_much_work():
    w1, w2 = Worker(), Worker(max_todo=2)
    w1.target = w2
    w1.done = 10
    assert not w2.todo
    w1.push()
    assert w1.done == 9 and w2.todo == 1
    w1.push()
    assert w1.done == 8 and w2.todo == 2
    w1.push()
    assert w1.done == 8 and w2.todo == 2
    w1.push()
    assert w1.done == 8 and w2.todo == 2
