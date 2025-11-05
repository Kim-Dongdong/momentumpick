package com.momentumpick.converter;

import com.momentumpick.dto.TempResponse;

public class TempConverter {

	public static TempResponse.TempTestDto toTempTestDto() {
		return TempResponse.TempTestDto.builder()
			.testString("This is Test!") // 이 string이 result에 담겨 응답된다.
			.build();
	}

	public static TempResponse.TempExceptionDTO toTempExceptionDto(Integer flag) {
		return TempResponse.TempExceptionDTO.builder()
			.flag(flag)
			.build();
	}
}
