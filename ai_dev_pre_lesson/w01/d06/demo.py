q33
不会，执行a.py时，导入b，b执行print("B start")后导入a，但是a本身在执行时候已经加入缓存pycache，不会被执行
所以顺序应该是 A start -> B start -> B end -> A end

q34
B, 执行a的时候，import b，加载的时候，b又import a，但是a没有被加载完成，没有x，所以报错

q35
同意，import的时候，后面没有被执行，比如变量还没赋值，提前访问会报错

q36
B

q37
import ai_dev_pre_lesson.w01.d06.student_analyzer.utils.validators

q38
from ...utils.validators import validate_student

q39
不属于，package是student_analyzer，不在package中，自然不属于package

q40
python -m ai_dev_pre_lesson.w01.d06.student_analyzer