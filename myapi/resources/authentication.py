import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from myapi import db
from myapi.model.user import UserModel
from myapi.model.authentication import ApprovalModel, PrivateModel, CompanyModel, BankModel, ManualModel
from myapi.model.enum import authentication_type, approval_result

class Approval(Resource):
    def get(self, id):
        approval = ApprovalModel.query.get(id)
        return jsonify(approval.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('authenType', type=int, location='json', required=True)
        post_parser.add_argument('authenID', type=int, location='json', required=True)
        post_parser.add_argument('approvalStatus', type=int, location='json', required=True)
        post_parser.add_argument('userid', type=int, location='json', required=True)
        post_parser.add_argument('adminid', type=int, location='json', required=True)
        post_parser.add_argument('description', type=str, location='json')
        args = post_parser.parse_args()

        a = ApprovalModel(
            args.authenType, args.authenID, args.approvalStatus, args.userid, args.adminid, args.description)
        db.session.add(a)

        user = UserModel.query.get(args.userid)
        user.authentications.append(a)
        if args.approvalStatus == approval_result.allow:
            user.authenticationType = user.authenticationType | args.authenType

        for key in authentication_type.__dict__:
            if not key.startswith('__') and args.authenType == authentication_type.__dict__[key]:
                p = model[key].query.filter_by(id = args.authenID).one()
                p.approvalStatus = args.approvalStatus
                break;

        db.session.commit()
        return jsonify(a.serialize())
        
class PrivateAuthenticate(Resource):
    def get(self, id):
        authority = PrivateModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('identityid', type=str, location='json', required=True)
        post_parser.add_argument('identityFrontImage', type=str, location='json', required=True)
        post_parser.add_argument('identityBackImage', type=str, location='json', required=True)
        args = post_parser.parse_args()

        p = PrivateModel(args.name, args.identityid, args.identityFrontImage, args.identityBackImage)
        db.session.add(p)

        user = UserModel.query.get(args.ownerid)
        user.privateAuthenHistory.append(p)
        db.session.commit()
        return jsonify(p.serialize())

    def delete(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        user = UserModel.query.get(args.ownerid)
        user.authenticationType = user.authenticationType ^ authentication_type.private
        db.session.commit()
        return jsonify(user.serialize())

class CompanyAuthenticate(Resource):
    def get(self, id):
        authority = CompanyModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('businessScope', type=str, location='json', required=True)
        post_parser.add_argument('licenseID', type=str, location='json', required=True)
        post_parser.add_argument('licenseImage', type=str, location='json', required=True)
        post_parser.add_argument('contactImage', type=str, location='json', required=True)
        args = post_parser.parse_args()

        c = CompanyModel(args.name, args.businessScope, args.licenseID, 
            args.licenseImage, args.contactImage)
        db.session.add(c)

        user = UserModel.query.get(args.ownerid)
        user.companyAuthenHistory.append(c)
        db.session.commit()
        return jsonify(c.serialize())

    def delete(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        user = UserModel.query.get(args.ownerid)
        user.authenticationType = user.authenticationType ^ authentication_type.company
        db.session.commit()
        return jsonify(user.serialize())

class BankAuthenticate(Resource):
    def get(self, id):
        authority = BankModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('bankAccount', type=str, location='json', required=True)
        post_parser.add_argument('bankName', type=str, location='json', required=True)
        post_parser.add_argument('bankLocation', type=str, location='json', required=True)
        args = post_parser.parse_args()

        b = BankModel(args.name, args.bankAccount, args.bankName, args.bankLocation)
        db.session.add(b)

        user = UserModel.query.get(args.ownerid)
        user.bankAuthenHistory.append(b)
        db.session.commit()
        return jsonify(b.serialize())

    def put(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('id', type=int, location='json', required=True)
        get_parser.add_argument('code', type=str, location='json', required=True)
        args = get_parser.parse_args()

        b = BankModel.query.get(args.id)
        if b.checkCode:
            return jsonify(result='already has check code')
        else:
            b.checkCode = args.code
            db.session.commit()
            return jsonify(b.serialize())

    def delete(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        user = UserModel.query.get(args.ownerid)
        user.authenticationType = user.authenticationType ^ authentication_type.bank
        db.session.commit()
        return jsonify(user.serialize())

class ManualAuthenticate(Resource):
    def get(self, id):
        authority = ManualModel.query.get(id)
        return jsonify(authority.serialize())

    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        post_parser.add_argument('name', type=str, location='json', required=True)
        post_parser.add_argument('phone', type=str, location='json', required=True)
        post_parser.add_argument('location', type=str, location='json', required=True)
        args = post_parser.parse_args()

        m = ManualModel(args.name, args.phone, args.location)
        db.session.add(m)

        user = UserModel.query.get(args.ownerid)
        user.manualAuthenHistory.append(m)
        db.session.commit()
        return jsonify(user.serialize())

    def delete(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('ownerid', type=int, location='json', required=True)
        args = post_parser.parse_args()

        user = UserModel.query.get(args.ownerid)
        user.authenticationType = user.authenticationType ^ authentication_type.manual
        db.session.commit()
        return jsonify(user.serialize())

class AuthenticationList(Resource):
    def get(self):
        # for x in dir(authentication_type):
        #     print getattr(authentication_type, str(x))
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('type', type=int, location='args', required=True)
        get_parser.add_argument('status', type=int, location='args', default=None)
        args = get_parser.parse_args()
        for key in authentication_type.__dict__:
            if not key.startswith('__') and args.type == authentication_type.__dict__[key]:
                result = model[key].query.filter_by(approvalStatus = args.status)
                return jsonify(type=args.type, data=[e.serialize() for e in result])
        return jsonify(type=args.type, data=[])

class UserAuthentication(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('type', type=int, location='args', required=True)
        get_parser.add_argument('userid', type=int, location='args', required=True)
        args = get_parser.parse_args()
        for key in authentication_type.__dict__:
            if not key.startswith('__') and args.type == authentication_type.__dict__[key]:
                result = model[key].query.filter_by(userid = args.userid)\
                        .order_by(model[key].authenticateDate.desc()).limit(1)
                return jsonify(type=args.type, data=[e.serialize() for e in result])
        return jsonify(type=args.type, data=[])

model = {
    'private' : PrivateModel,
    'company' : CompanyModel,
    'bank' : BankModel,
    'manual' : ManualModel
}

