import os
import subprocess
import json
import logging

# Path to batfile that initiates the qgis environment
qgis_call = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'qgis_run_processing_algorithm.bat')


def qgis_runalg(algorithm, *args, **kwargs):
    """Run QGIS Processing `algorithm` with `parameters`

    Parameters
    ----------
    algorithm : str
        algorithm name
    args : list
        positional args
    kwargs : dict
        if present, override args
        kwargs are passed to qgis calling interface
        as json

    Logging
    -------
    if 'logger' in kwargs:
        write info to that logger.

    Returns
    -------
    lines : iterator

    Note
    ----
    This function returns an iterator over the output from the command (STDOUT and STDERR).
    This means you must wrap it in a list() or for loop for the command to run at all.
    """
    logger = kwargs.pop('logger', None)
    if logger is None:
        logger = logging.getLogger(__name__)

    # make command
    cmd = [qgis_call, algorithm]
    if kwargs:
        kwargs_json = json.dumps(kwargs)
        cmd += ['--from_json', kwargs_json]
    elif args:
        cmd += args

    # debugging output
    logger.debug('Command is \'{}\''.format(' '.join(cmd)))

    # run command
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        else:
            yield line


def filter_errors(line_iter):
    errorlines = []
    for line in line_iter:
        if errorlines or 'error' in line.lower():
            errorlines.append(line)
            yield line
    if errorlines:
        msg = 'An error occurred:\n\n    ' + '    '.join(errorlines)
        raise RuntimeError(msg)
