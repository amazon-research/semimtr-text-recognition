from fastai.vision import *

from semimtr.modules.model_abinet_iter import ABINetIterModel


class ConsistencyRegularizationFusionModel(ABINetIterModel):
    def __init__(self, config):
        super().__init__(config)
        self.loss_weight = ifnone(config.model_teacher_student_loss_weight, 1.0)

    def forward(self, images, forward_only_teacher=False, *args):
        if forward_only_teacher:
            a_res_teacher, l_res_teacher, v_res_teacher = super().forward(images)
            a_res_student, l_res_student, v_res_student = 0, 0, 0
        else:
            images_teacher_view, images_student_view = images[:, 0], images[:, 1]
            a_res_teacher, l_res_teacher, v_res_teacher = super().forward(images_teacher_view)
            a_res_student, l_res_student, v_res_student = super().forward(images_student_view)

        return {'teacher_outputs': [a_res_teacher, l_res_teacher, v_res_teacher],
                'student_outputs': [a_res_student, l_res_student, v_res_student],
                'loss_weight': self.loss_weight,
                'name': 'teacher_student_fusion'}
