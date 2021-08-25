odoo.define('complementary_contact_data.contact_info_widget', function (require) {
"use strict";

    var session = require('web.session');
    var registry = require('web.field_registry');
    var rpc = require("web.rpc");
    var core = require('web.core');
    var relationalFields = require('web.relational_fields');
    var qweb = core.qweb;
    var ajax = require('web.ajax');
    var dialogs = require('web.view_dialogs');
    var _t = core._t;

    ajax.loadXML('/complementary_contact_data/static/src/xml/contact_info_widget.xml', qweb);

    var contactInfoWidget = relationalFields.FieldMany2ManyTags.extend({
        tag_template: "ContactInfoWidget",
        fieldsToFetch: {
            short_name: {type: 'char'},
            name: {type: 'char'},
            contact_info_type: {type: 'char'},
            url_type: {type: 'char'},
            comment: {type: 'char'},
            sequence: {type: 'integer'},
        },
        events: _.extend({}, relationalFields.FieldMany2ManyTags.prototype.events, {
            'click .o_edit': '_onEditTag',
            'click .o_create': '_onEditTag',
            'click .o_copy': '_onCopyTag',
            'click .o_expand': '_onclickHide',
            'click .o_sequence': '_onClickUpper',
            'dragstart .hide_expand_li':  '_onDragStart',
            'drop .hide_expand_li': '_onDrop',
            'dragenter .hide_expand_li': function(event){event.preventDefault();},
            'dragover .hide_expand_li': function(event){event.preventDefault();},
        }),

        init: function () {
            // To remove input tag from the field class
            this._super.apply(this, arguments);
            if (this.mode === 'edit') {
                this.className -= ' o_input';
            };
            this.expanded_area = true;
            this.maximum_number = 7;
        },

        _getRenderTagsContext: function () {
            // To control too long lists
            var resElements = this._super.apply(this, arguments);

            // We sort to the case sequence is changed
            resElements.elements.sort(function(a, b) {return a.sequence - b.sequence});
            if (resElements.elements.length > this.maximum_number && this.mode === 'readonly') {
                // In edit mode we do not show show/expand
                resElements.hide_elements = true;
            }
            else {
                resElements.hide_elements = false;
            }
            return resElements
        },

        _renderTags: function () {
            // Re write to make excess records hide
            this._super.apply(this, arguments);
            if (this.mode === 'readonly'){
                this._onExpandHide();
            };
        },

        _renderEdit: function () {
            // Re-write, since we do not need M2o features here
            // if (this.nodeOptions.always_reload) {
            //     value = this._getDisplayName(value);
            // }
            this.expanded_area = false; // In edit mode we show the whole list
            this._renderTags();
        },

        _removeTag: function (id) {
            // To delete instead of just forgetting (since it is o2m - not m2m)
            var record = _.findWhere(this.value.data, {res_id: id});
            this._setValue({
                operation: 'DELETE',
                ids: [record.id],
            });
        },

        _updateTag: function(id, changes) {
            // The method to write in existing record
            var record = _.findWhere(this.value.data, {res_id: id});
            // Since not all fields are introduced on the form, we should removes not-exisiting one
            // * BE CUATIOUS *: other fields would be anyway written! Thus, in ideal world all updated fields should
            // be presented in a list. Otherwise, discard changes would not work
            for (var fieldName in changes) {
                var field = record.fields[fieldName];
                if (!field) {
                    delete changes[fieldName];
                };
            };
            this._setValue({
                operation: 'UPDATE',
                id: record.id,
                data: changes,
            });
        },

        _onEditTag: function (event) {
            // To the needs of editing and creating new contact info
            event.stopPropagation();
            var self = this;
            var context = this.record.getContext(this.recordParams);
            var resId = $(event.target).parent().data('id');

            // to the need of default sequence we want to get the previous record sequence
            var allItems = self.$el.find('.hide_expand_li');
            var defaultSequence = 0;
            if (allItems.length) {
                defaultSequence = parseInt(allItems[allItems.length-1].getAttribute("id")) + 1;
            };

            this._rpc({
                    model: this.field.relation,
                    method: 'get_formview_id',
                    args: [[this.value.res_id]],
                    context: context,
                })
                .then(function (view_id) {
                    var onSaved = function(record) {
                        var new_data = record.data;
                        if (resId) {
                            self._updateTag(resId, new_data);
                        }
                        else {
                            self._addTag(new_data);
                        }
                    }
                    // To manage discarding changes for editing, but not for create
                    var shouldSaveLocally = true;
                    if (! resId) {
                        shouldSaveLocally = false;
                    };

                    context.default_sequence = defaultSequence;
                    new dialogs.FormViewDialog(self, {
                        res_model: self.field.relation,
                        res_id: resId,
                        context: context,
                        title: _t("Open: ") + self.string,
                        view_id: view_id,
                        readonly: false,
                        on_saved: onSaved,
                        shouldSaveLocally: shouldSaveLocally,
                    }).open();
                });
        },

        _onCopyTag: function(event) {
            // To copy the value to clipboard
            var nameToCopy = $(event.target).data('name');
            // Hack to avoid cross-browsing troubles
            var dummy = document.createElement("input");
            document.body.appendChild(dummy);
            dummy.setAttribute('value', nameToCopy);
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
        },

        _onclickHide: function(event) {
            // Dummy method to catch user click of expanding / hiding
            this._onExpandHide()
        },

        _onExpandHide: function() {
            // Method to show / hide elements when there are too many of those
            this.expanded_area = !this.expanded_area;
            var ulMain =  this.$el;
            var allItems = ulMain.find('.hide_expand_li');
            var showButton = ulMain.find('.show_button_contact');
            var hideButton = ulMain.find('.hide_button_contact');

            if (this.expanded_area) {
                allItems.removeClass('cc_hidden');
                showButton.addClass('cc_hidden');
                hideButton.removeClass('cc_hidden');
            }
            else {
                var itemsNumber = allItems.length - this.maximum_number;
                if (itemsNumber > 0) {
                    var toHideItems = allItems.slice(-itemsNumber);
                    toHideItems.addClass('cc_hidden');
                    showButton.removeClass('cc_hidden');
                    hideButton.addClass('cc_hidden');
                };
            }
        },

        _onClickUpper: function(event) {
            // The method to put contact info upper
            var currentLi = $(event.target).parent().parent().parent();
            var currentID =  parseInt(currentLi[0].id);
            var previousID = currentID - 1;
            if (previousID >= 0) {
                var previousLi = this.$el.find('#' + previousID.toString() + '.hide_expand_li');
                var currentResID = currentLi.data("id");
                var previousResID = previousLi.data("id");
                // To do: is it possibele to proceed multiple update?
                this._updateTag(currentResID, {"sequence": previousID});
                this._updateTag(previousResID, {"sequence": currentID});
            };
        },

        _onDragStart: function(event){
            event.originalEvent.dataTransfer.setData('text/html', event.currentTarget.id);
            event.originalEvent.dataTransfer.effectAllowed = 'link';
            event.originalEvent.dataTransfer.dropEffect = 'link';
            this.currentDraggedId = event.currentTarget.id;
        },

        _onDrop: function(event) {
            // Manage drop of contact info
            if (this.mode === 'edit') {
                var newerPlaceId = parseInt(event.currentTarget.id);
                var previousPlaceId = parseInt(this.currentDraggedId);
                var initialdLi = this.$el.find('#' + previousPlaceId.toString() + '.hide_expand_li');

                if (newerPlaceId > previousPlaceId) {
                    // all items lesser or equal than newerPlaceId should be decreased by one
                    var iterator = previousPlaceId + 1;
                    while (iterator < newerPlaceId + 1) {
                        var updatedLi = this.$el.find('#' + iterator.toString() + '.hide_expand_li');
                        var resId = updatedLi.data("id");
                        this._updateTag(resId, {"sequence": iterator-1});
                        iterator++;
                    }
                }
                if  (newerPlaceId < previousPlaceId) {
                    // all items bigger than newerPlaceId should be increaed by one
                    var iterator = previousPlaceId - 1;
                    while (iterator > newerPlaceId - 1) {
                        var updatedLi = this.$el.find('#' + iterator.toString() + '.hide_expand_li');
                        var resId = updatedLi.data("id");
                        this._updateTag(resId, {"sequence": iterator+1});
                        iterator--;
                    }
                };
                if  (newerPlaceId !== previousPlaceId) {
                    // Update the initial element itself
                    var resId = initialdLi.data("id");
                    this._updateTag(resId, {"sequence": newerPlaceId});
                };

            }
        },
    });

    registry.add('contactInfoWidget', contactInfoWidget);

});
