#coding=utf-8
import os
from flask import request, jsonify#, send_from_directory
from flask.ext.restful import Resource, reqparse
# from werkzeug.datastructures import FileStorage
from myapi import db#, app
from myapi.model.enum import file_type
from myapi.model.user import UserModel
from myapi.common.file import resize, isAllowedFile, getServerFilePath

class UploadFile(Resource):
    def post(self):
        file = request.files['file']
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('type', type=int, location='args', required=True)
        get_parser.add_argument('foldername', type=int, location='args', required=True)
        get_parser.add_argument('thumbnail', type=int, location='args', default=0)
        args = get_parser.parse_args()

        if file and isAllowedFile(args.type, file.filename):
            serverFilePath = getServerFilePath(args.type, args.foldername, file.filename)
            
            if args.type == file_type.profileLarge:
                user = UserModel.query.get(args.foldername)
                file.save(serverFilePath)
                user.imageLarge = os.path.basename(serverFilePath)

                mediumImageFilePath = getServerFilePath(file_type.profileMedium, args.foldername, file.filename)
                mediumImageFile = resize(file, 63, 63)
                mediumImageFile.save(mediumImageFilePath)
                user.imageMedium = os.path.basename(mediumImageFilePath)

                smallImageFilePath = getServerFilePath(file_type.profileSmall, args.foldername, file.filename)
                smallImageFile = resize(file, 36, 36)
                smallImageFile.save(smallImageFilePath)
                user.imageSmall = os.path.basename(smallImageFilePath)
                db.session.commit()
                return jsonify(user=UserModel.query.get(args.foldername).serialize())
            else:
                file.save(serverFilePath)

            if args.thumbnail:
                thumbnailfile = resize(file, 223, 99999)
                tsf = getServerFilePath(file_type.workThumbnail, args.foldername, file.filename)
                thumbnailfile.save(tsf)
                return jsonify(fileName=os.path.basename(serverFilePath), thumbnailFileName=os.path.basename(tsf))
            else:
                return jsonify(fileName=os.path.basename(serverFilePath))
        return jsonify(message='不支持文件类型！')

    # def get(self, foldername, imagetype, filename):
    #     if filename:
    #         fpath = os.path.join(app.config['ROOT_PATH'], 
    #             app.config['UPLOAD_FOLDER'], path[imagetype](foldername))
    #         return send_from_directory(fpath, filename)
    #     else:
    #         return ''