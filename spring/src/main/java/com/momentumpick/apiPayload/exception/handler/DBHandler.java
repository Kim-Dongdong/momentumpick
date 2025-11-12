package com.momentumpick.apiPayload.exception.handler;

import com.momentumpick.apiPayload.code.BaseErrorCode;
import com.momentumpick.apiPayload.exception.GeneralException;

public class DBHandler extends GeneralException {
	public DBHandler(BaseErrorCode errorCode) {
		super(errorCode);
	}
}
