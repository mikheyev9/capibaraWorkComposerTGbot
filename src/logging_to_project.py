import logging as logger_to_project

logger_to_project.basicConfig(
    level=logger_to_project.INFO,
    filename=f"{__name__}.log",
    filemode="a",
    encoding='utf-8',
    format=u"%(asctime)s %(levelname)s - %(filename)s %(funcName)s: %(lineno)d - %(message)s"
)
