import math
import sys
import time
import numpy as np

sys.path.append('../')
from metrics.metrics import compute_stats, compute_mIoU, compute_accuracy_segmentation
from simple_trainer_manager import SimpleTrainer

class SemanticSegmentation_Manager(SimpleTrainer):
    def __init__(self, cf, model):
        super(SemanticSegmentation_Manager, self).__init__(cf, model)

    class train(SimpleTrainer.train):
        def __init__(self, logger_stats, model, cf, validator, stats):
            super(SemanticSegmentation_Manager.train, self).__init__(logger_stats, model, cf, validator, stats)
            self.best_IoU = 0

        def validate_epoch(self, valid_set, valid_loader, criterion, early_Stopping, epoch):

            if valid_set is not None and valid_loader is not None:
                # Set model in validation mode
                self.model.net.eval()

                self.validator.start(criterion, valid_set, valid_loader, epoch)

                # Early stopping checking
                if self.cf.early_stopping:
                    early_Stopping.check(self.stats.train.loss, self.stats.val.loss, self.stats.val.mIoU,
                                         self.stats.val.acc)
                    if early_Stopping.stop == True:
                        self.stop = True

                # Set model in training mode
                self.model.net.train()

        def update_messages(self, epoch, epoch_time):
            # Update logger
            epoch_time = time.time() - epoch_time
            self.logger_stats.write('\t Epoch step finished: %ds ' % (epoch_time))

            # Compute best stats
            self.msg_stats_last = '\nLast epoch: mIoU = %.2f, acc= %.2f, loss = %.5f\n' % (
            100 * self.stats.val.mIoU, 100 * self.stats.val.acc, self.stats.val.loss)
            if self.best_IoU < self.stats.val.mIoU:
                self.msg_stats_best = 'Best case: epoch = %d, mIoU = %.2f, acc= %.2f, loss = %.5f\n' % (
                    epoch, 100 * self.stats.val.mIoU, 100 * self.stats.val.acc, self.stats.val.loss)
                self.best_IoU = self.stats.val.mIoU

    class validation(SimpleTrainer.validation):
        def __init__(self, logger_stats, model, cf, stats):
            super(SemanticSegmentation_Manager.validation, self).__init__(logger_stats, model, cf, stats)

        def compute_stats(self, TP_list, TN_list, FP_list, FN_list, val_loss):
            mean_IoU = compute_mIoU(TP_list, FP_list, FN_list)
            mean_accuracy = compute_accuracy_segmentation(TP_list, FN_list)
            self.stats.val.acc = np.mean(mean_accuracy)
            self.stats.val.mIoU = np.mean(mean_IoU)
            self.stats.val.loss = val_loss.avg

        def save_stats(self, epoch):
            # Save logger
            if epoch is not None:
                self.logger_stats.write('----------------- Epoch scores summary -------------------------')
                self.logger_stats.write('[epoch %d], [val loss %.5f], [acc %.2f], [mean_IoU %.2f],' % (
                    epoch, self.stats.val.loss, 100*self.stats.val.acc, 100*self.stats.val.mIoU))
                self.logger_stats.write('---------------------------------------------------------------- \n')
            else:
                self.logger_stats.write('----------------- Scores summary --------------------')
                self.logger_stats.write('[val loss %.5f], [acc %.2f], [mean_IoU %.2f]' % (
                    self.stats.val.loss, 100 * self.stats.val.acc, 100 * self.stats.val.mIoU))
                self.logger_stats.write('---------------------------------------------------------------- \n')