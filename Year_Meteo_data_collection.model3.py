"""
Model exported as python.
Name : Year_Meteo_data_collection
Group : SASSCAL Weathernet
With QGIS : 34403
"""

from typing import Any, Optional

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingContext
from qgis.core import QgsProcessingFeedback, QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterExpression
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsExpression
from qgis import processing


class Year_meteo_data_collection(QgsProcessingAlgorithm):

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
        # Enumerator with the names of stations. Connect to the ID codes used in the URL through model variables.
        self.addParameter(QgsProcessingParameterEnum('choose_aws', 'Choose AWS', options=['Campus ISPT','Mukongo','Onjiva'], allowMultiple=False, usesStaticStrings=False, defaultValue=None))
        # The year of data to download
        self.addParameter(QgsProcessingParameterNumber('year', 'Year', type=QgsProcessingParameterNumber.Integer, minValue=2014, defaultValue=None))
        # Chooses the corresponding variable to fill the URL
        param = QgsProcessingParameterExpression('aws_id_parameter', 'AWS_ID_parameter', optional=True, parentLayerParameterName='', defaultValue='Case when  @choose_aws is 0\r\nthen  to_string(@Campus_ISPT )\r\nwhen  @choose_aws is 1\r\nthen to_string(@Mukongo)\r\nwhen  @choose_aws is 2\r\nthen to_string(@Onjiva)\r\nend ')
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)

    def processAlgorithm(self, parameters: dict[str, Any], context: QgsProcessingContext, model_feedback: QgsProcessingFeedback) -> dict[str, Any]:
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Download file (SASSCAL Data)
        alg_params = {
            'DATA': None,
            'METHOD': 0,  # GET
            'OUTPUT': QgsExpression("@project_folder|| '/'||'MONTHLY'||\r\n\r\nCase when  @choose_aws is 0\r\nthen  to_string('Campus_ISPT' )\r\nwhen  @choose_aws is 1\r\nthen to_string('Mukongo')\r\nwhen  @choose_aws is 2\r\nthen to_string('Onjiva')\r\nend \r\n\r\n||'_'||to_string( @year )||'.csv'").evaluate(),
            'URL': QgsExpression("to_string('https://sasscalweathernet.org/w_download_csv.php?loggerid_crit='+\r\n\r\nCase when  @choose_aws is 0\r\nthen  to_string(@Campus_ISPT )\r\nwhen  @choose_aws is 1\r\nthen to_string(@Mukongo)\r\nwhen  @choose_aws is 2\r\nthen to_string(@Onjiva)\r\nend \r\n\r\n+'&date_crit='\r\n+to_string( @year )\r\n+'&stype=3')").evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DownloadFileSasscalData'] = processing.run('native:filedownloader', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self) -> str:
        return 'Year_Meteo_data_collection'

    def displayName(self) -> str:
        return 'Year_Meteo_data_collection'

    def group(self) -> str:
        return 'SASSCAL Weathernet'

    def groupId(self) -> str:
        return 'SASSCAL Weathernet'

    def shortHelpString(self) -> str:
        return """<html><body><p><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:9.5pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:18pt; font-weight:600;">SASSCAL Weathernet</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; font-style:italic;">Year_Meteo_data_collection</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">This model allows the quick acquisition of CSV files containing meteorological observations from Automatic Weather Stations availbale on the SASSCAL Weathernet platform.</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">It downloads and writes the file in the machine where the model is being run, storing at the QGIS project folder directory under the name &quot;Monthly[AWS name]_[Year].csv&quot;</p></body></html></p>
<h2>Input parameters</h2>
<h3>Choose AWS</h3>
<p>Indicate the available Autoamtic Weather Station</p>
<h3>Year</h3>
<p>Choose the year of interest</p>
<h2>Examples</h2>
<p><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:9.5pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">MonthlyCampus_ISPT_2014.csv</p></body></html></p><br><p align="right">Algorithm author: Evanilton Edgar Serrão Pires. Developed for the WIRE project, part of SASSCAL 2.0 portfolio. Project partners: Achim Schulte, Christian Reinhardt-imjela, Monique Fahrenberg (FUB), Robert Juepner (TUK), Valentine Katte (UNAM) & Evanilton Pires (ISPT).

SASSCAL Weathernet Year Meteo data collection © 2025 by Evanilton E. S. Pires is licensed under CC BY-NC-SA 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
</p><p align="right">Help author: pires.evanilton@gmail.com</p><p align="right">Algorithm version: V0</p></body></html>"""

    def helpUrl(self) -> str:
        return 'To use the model, import the model (model file) to a QGIS project and run.'


    def createInstance(self):
        return self.__class__()
