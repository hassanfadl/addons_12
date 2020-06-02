
odoo.define('sale_filters.dashboard', function (require) {
"use strict";
console.log("sfdfdgfgfgffhfh"
var core = require('web.core');
var framework = require('web.framework');
var session = require('web.session');
var ajax = require('web.ajax');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;

var SaleDashboardView = AbstractAction.extend(ControlPanelMixin, {
	events: {
		'click .sale-quotation': 'sale_quotation',
	},
	init: function(parent, context) {
        this._super(parent, context);
    },
    willStart: function() {
        var self = this;
        return $.when(ajax.loadLibs(this), this._super()).then(function() {
            return self.fetch_data();
        });
    },
    },
    start: function() {
        var self = this;
        return this._super();
    },
    fetch_data: function() {
        var self = this;
        var def1 =  this._rpc({
                model: 'sale.order',
                method: 'get_user_partner_details'
        }).done(function(result) {
            self.login_partner =  result[0];
        });
        },
    render: function() {
        var super_render = this._super;
        var self = this;
        var sale_filters = QWeb.render( 'sale_filters.dashboard', {
            widget: self,
        });
        $( ".o_control_panel" ).addClass( "o_hidden" );
        $(sale_filters).prependTo(self.$el);
        return sale_filters
    },
    reload: function () {
            window.location.href = this.href;
    },
    sale_quotation: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return self.do_action({
            name: _t("Quotations"),
            type: 'ir.actions.act_window',
            res_model: 'sale.order',
            view_mode: 'tree,form',
            view_type: 'tree',
            views: [[false, 'list'],[false, 'form']],
            domain: [['partner_id','=', this.login_partner.id]],
            target: 'current'
        }, options)
        
    },
    })
    });  
