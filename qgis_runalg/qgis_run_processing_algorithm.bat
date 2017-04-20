@echo off

call "C:\OSGeo4W64\bin\o4w_env.bat"

@echo off

path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES

rem Set VSI cache to be used as buffer, see #6448
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt4\plugins

if "%1"=="" (
	REM SET CMD="script:downloadrainfall" "--from_json" "{'extent':'-180,180,-50,50', 'startDate':'20150525', 'endDate':'20150526', 'deleteDownloadedFiles':'True', 'splitIntoYears':'False', 'loadOutput':'False', 'outputNetCDF':'C:/temp/TRMM/rain.nc'}"
        REM SET CMD="script:downloadrainfall" "-180,180,-50,50" "20150525" "20150526" True False False "C:/temp/TRMM/rain.nc"
	SET CMD="snap:reproject"
) else (
	SET CMD=%*
)

python %~dp0\qgis_run_processing_algorithm.py %CMD%
