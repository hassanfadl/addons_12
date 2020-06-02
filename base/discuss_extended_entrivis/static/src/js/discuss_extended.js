odoo.define('discuss_extended_entrivis.discuss_extended_entrivis', function (require) {
"use strict";

console.log('loaded')

var BasicComposer = require('mail.composer.Basic');
var mailUtils = require('mail.utils');

BasicComposer.include({
        events: _.extend({}, BasicComposer.prototype.events, {
            'click .o_composer_button_full_composer': '_onOpenFullComposer',
        }),

    _onOpenFullComposer: function () {

        if (!this._doCheckAttachmentUpload()){
            return false;
        }

        var self = this;
        console.log('selfselfselfselfself', self, self.options.thread, self.options.thread._id);
        self.options.isLog = true;
        var recipientDoneDef = $.Deferred();

        var message = this.call('mail_service', 'getMessage', false);
        
            var context = {
                // default_parent_id: self.id,
                default_model: 'mail.channel',
                default_res_id: self.options.thread._id,
                default_subtype: 'mail.mt_comment',
                // default_channel_ids : [self.options.thread._id],
                default_body: mailUtils.getTextToHTML(self.$input.val()),
                // default_attachment_ids: _.pluck(self.get('attachment_ids'), 'id'),
                // default_partner_ids: partnerIDs,
                default_is_log: true,
                // mail_post_autofollow: true,
            };

            var action = {
                type: 'ir.actions.act_window',
                res_model: 'discuss.extend',
                view_mode: 'form',
                view_type: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: context,
            };
            self.do_action(action, {
                on_close: self.trigger.bind(self, 'need_refresh'),
            }).then(function () {
                 self.trigger.bind(self, 'close_composer')
            });
   
        },

});

});
