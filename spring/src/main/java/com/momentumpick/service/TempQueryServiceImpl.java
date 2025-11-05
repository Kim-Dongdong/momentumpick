package com.momentumpick.service;

import org.springframework.stereotype.Service;

import com.momentumpick.apiPayload.code.status.ErrorStatus;
import com.momentumpick.apiPayload.exception.handler.TempHandler;

@Service
public class TempQueryServiceImpl implements TempQueryService {

	@Override
	public void CheckFlag(Integer flag) {
		if (flag == 1) {
			throw new TempHandler(ErrorStatus.TEMP_EXCEPTION);
		}
	}
}
