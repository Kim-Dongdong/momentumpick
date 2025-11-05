package com.momentumpick.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

public class TempResponse {

	@Builder
	@Getter
	@AllArgsConstructor
	@NoArgsConstructor
	public static class TempTestDto {
		String testString;
	}

	@Builder
	@Getter
	@AllArgsConstructor
	@NoArgsConstructor
	public static class TempExceptionDTO {
		Integer flag;
	}
}
