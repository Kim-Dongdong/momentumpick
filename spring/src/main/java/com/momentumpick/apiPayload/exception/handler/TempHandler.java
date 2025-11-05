package com.momentumpick.apiPayload.exception.handler;

import com.momentumpick.apiPayload.code.BaseErrorCode;
import com.momentumpick.apiPayload.exception.GeneralException;

public class TempHandler extends GeneralException {

    public TempHandler(BaseErrorCode errorCode) {
        super(errorCode);
    }
}
