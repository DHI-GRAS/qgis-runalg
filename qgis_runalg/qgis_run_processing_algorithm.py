from __future__ import print_function
import sys
import os
import json
import argparse
import logging

def qgis_runalg(algorithm, *args, **kwargs):
    """Run QGIS Processing algorithm

    Parameters
    ----------
    algorithm : str
        algorithm name e.g. script:myscript
    args : positional arguments
        passed to processing.runalg
    kwargs : keword arguments
        passed to processing.runalg

    Logging
    -------
    if 'logger' in kwargs:
        write info to that logger.
    """
    # Initialize QGIS and Processing if running as a subprocess
    # First find paths of QGIS Python libraries and of Processing
    # Assumes OsGeo4W installation
    qgisPath = os.path.dirname(os.path.dirname(sys.executable))
    qgisPath = os.path.join(qgisPath, "apps", "qgis", "python")
    sys.path.append(qgisPath)
    # Check if processing plugin is in the user directory (priority) or
    # QGIS directory (backup)
    if os.path.isdir(os.path.join(os.path.expanduser("~"), ".qgis2", "python", "plugins", "processing")):
        processingPath = os.path.join(os.path.expanduser("~"), ".qgis2", "python", "plugins")
    else:
        processingPath = os.path.join(qgisPath, "plugins")
    sys.path.append(processingPath)

    # logging
    logger = kwargs.pop('logger', None)
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    # Initialise QGIS
    from qgis.core import QgsApplication
    app = QgsApplication([], True)
    app.setPrefixPath(os.path.dirname(qgisPath))
    app.initQgis()

    # Import Processing
    import processing
    from processing.core.Processing import Processing

    # Initialise Processing
    Processing.initialize()

    # Try to add SNAP and BEAM
    try:
        from processing_gpf.BEAMAlgorithmProvider import BEAMAlgorithmProvider
        from processing_gpf.SNAPAlgorithmProvider import SNAPAlgorithmProvider
        bp = BEAMAlgorithmProvider()
        sp = SNAPAlgorithmProvider()
        Processing.addProvider(bp, True)
        Processing.addProvider(sp, True)
        logger.debug('Successfully loaded SNAP and BEAM algorithm providers.')
    except ImportError:
        logger.debug('SNAP and BEAM not found. These algorithms '
                'will not be available.')
        pass

    # Set progress to be displayed in the command prompt
    progress = CmdProgress()

    # Run the algorithm
    return processing.runalg(algorithm, *args, progress=progress, **kwargs)


class CmdProgress:

    def error(self, msg):
        print(msg)

    def setText(self, text):
        pass

    def setPercentage(self, i):
        pass

    def setInfo(self, _):
        pass

    def setCommand(self, _):
        pass

    def setDebugInfo(self, _):
        pass

    def setConsoleInfo(self, text):
        print(text)

    def close(self):
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run QGIS algorithm from command line')
    parser.add_argument('algorithm', help='Algorithm name')
    parser.add_argument('--from_json', metavar='JSON_STRING', help='Parameters as JSON string. Disables positional arguments.')
    args, positional = parser.parse_known_args()

    # parse json if present, else use positional
    keyword = {}
    if args.from_json is not None:
        keyword = json.loads(args.from_json.replace('\'','"'))

    print(args.algorithm)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug('Algorithm: {}'.format(args.algorithm))
    logger.debug('Positional args: {}'.format(positional))
    logger.debug('Keyword args: {}'.format(keyword))
    try:
        qgis_runalg(args.algorithm, *positional, **keyword)
    except:
        e = sys.exc_info()[0]
        logging.exception(e)
