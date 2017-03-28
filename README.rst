pytest-only
===========

Only run tests marked with ``@pytest.mark.only``. If none are marked, all tests run as usual.

Borrowed from `mocha <https://mochajs.org/>`_.


Installation
------------

.. code-block:: bash

    pip install pytest-only


Usage
-----

Use it on functions

.. code-block:: python

    import pytest

    def test_that_will_not_run():
        assert 0

    @pytest.mark.only
    def test_that_will_run():
        assert 1


.. code-block:: bash

    $ py.test -v test_example.py

    ============================= test session starts ==============================
    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /tmp/example/bin/python3.6
    cachedir: .cache
    rootdir: /tmp/example, inifile:
    plugins: only-1.0.0
    collected 2 items

    test_example.py::test_that_will_run PASSED

    =========================== 1 passed in 0.00 seconds ===========================


Or use it on classes

.. code-block:: python

    import pytest

    class TestThatWillNotRun:
        def test_that_will_not_run(self):
            assert 0


    @pytest.mark.only
    class TestThatWillRun:
        def test_that_will_run(self):
            assert 1


.. code-block:: bash

    $ py.test -v test_example.py

    ============================= test session starts ==============================
    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /tmp/example/bin/python3.6
    cachedir: .cache
    rootdir: /tmp/example, inifile:
    plugins: only-1.0.0
    collected 2 items

    test_example.py::TestThatWillRun::test_that_will_run PASSED

    =========================== 1 passed in 0.00 seconds ===========================


Or use it on modules

.. code-block:: python

    # test_example.py
    import pytest

    pytestmark = pytest.mark.only

    def test_that_will_run():
        assert 1


.. code-block:: python

    # test_example2.py
    def test_that_will_not_run():
        assert 0


.. code-block:: bash

    $ py.test -v test_example.py test_example2.py

    ============================= test session starts ==============================
    platform linux -- Python 3.6.1, pytest-3.0.7, py-1.4.33, pluggy-0.4.0 -- /home/they4kman/.virtualenvs/tmp-53d5944c7c78d28/bin/python3.6
    cachedir: .cache
    rootdir: /home/they4kman/.virtualenvs/tmp-53d5944c7c78d28, inifile:
    plugins: only-1.0.0
    collected 2 items

    test_example.py::test_that_will_run PASSED

    =========================== 1 passed in 0.00 seconds ===========================