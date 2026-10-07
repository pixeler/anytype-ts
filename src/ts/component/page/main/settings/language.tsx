import React, { forwardRef, useRef } from 'react';
import { Title, Label, Select, Switch } from 'Component';
import * as I from 'Interface';

const PageMainSettingsLanguage = forwardRef<{}, I.PageSettingsComponent>((props, ref) => {

	const { config, interfaceLang, layoutDirection, calendarType, showRelativeDates, dateFormat, timeFormat, firstDay } = S.Common;
	const { languages } = config;
	const interfaceLanguages = U.Menu.getInterfaceLanguages();
	const spellingRef = useRef(null);
	const firstDayOptions = [
		{ id: 6, name: translate('day6') },
		{ id: 7, name: translate('day7') },
		{ id: 1, name: translate('day1') },
	];

	const getSpellingLanguages = () => {
		const { languages } = config;
		const langSet = new Set(languages);

		return U.Menu.getSpellingLanguages().sort((c1, c2) => {
			const idx1 = langSet.has(c1.id);
			const idx2 = langSet.has(c2.id);

			if (!c1.id && c2.id) return -1;
			if (c1.id && !c2.id) return 1;

			if (idx1 && !idx2) return -1;
			if (!idx1 && idx2) return 1; 
			return 0;
		});
	};

	return (
		<>
			<Title text={translate('pageSettingsLanguageTitle')} />

			<Label className="section" text={translate('popupSettingsPersonalSectionLanguage')} />
			<div className="actionItems">

				<div className="item">
					<Label text={translate('popupSettingsPersonalSpellcheckLanguage')} />

					<Select
						id="spellcheck"
						ref={spellingRef}
						value={languages}
						options={getSpellingLanguages()}
						onChange={v => {
							Action.setSpellingLang(v);

							const options = getSpellingLanguages();

							spellingRef.current?.setOptions(options);
							S.Menu.updateData('select', { options });
						}}
						arrowClassName="black"
						isMultiple={true}
						noFilter={false}
						menuParam={{ horizontal: I.MenuDirection.Right, width: 300 }}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalInterfaceLanguage')} />

					<Select
						id="interfaceLang"
						value={interfaceLang}
						options={interfaceLanguages}
						onChange={v => {
							Action.setInterfaceLang(v);
							const isRtl = [ 'fa-IR', 'ar-SA', 'he-IL' ].includes(v) || v.startsWith('fa') || v.startsWith('ar') || v.startsWith('he');
							S.Common.layoutDirectionSet(isRtl ? 'rtl' : 'ltr');
							if (v === 'fa-IR' || v.startsWith('fa')) {
								S.Common.calendarTypeSet('persian');
							}
						}}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right, width: 300 }}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalLayoutDirection')} />

					<Select
						id="layoutDirection"
						value={layoutDirection}
						options={[
							{ id: 'rtl', name: translate('popupSettingsPersonalLayoutRtl') },
							{ id: 'ltr', name: translate('popupSettingsPersonalLayoutLtr') },
						]}
						onChange={v => S.Common.layoutDirectionSet(v as 'ltr' | 'rtl')}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right, width: 300 }}
					/>
				</div>
			</div>

			<Label className="section" text={translate('popupSettingsPersonalSectionDateTime')} />
			<div className="actionItems">

				<div className="item">
					<Label text={translate('popupSettingsPersonalCalendarType')} />
					<Select
						id="calendarType"
						value={calendarType}
						options={[
							{ id: 'gregorian', name: translate('popupSettingsPersonalCalendarGregorian') },
							{ id: 'persian', name: translate('popupSettingsPersonalCalendarPersian') },
						]}
						onChange={v => S.Common.calendarTypeSet(v as 'gregorian' | 'persian')}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right, width: 300 }}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalDateFormat')} />
					<Select
						id="dateFormat"
						value={String(dateFormat)}
						options={U.Menu.dateFormatOptions()}
						onChange={v => {
							S.Common.dateFormatSet(v);
							analytics.event('ChangeDateFormat', { type: v });
						}}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right }}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalTimeFormat')} />
					<Select
						id="timeFormat"
						value={String(timeFormat)}
						options={U.Menu.timeFormatOptions()}
						onChange={v => {
							S.Common.timeFormatSet(v);
							analytics.event('ChangeTimeFormat', { type: v });
						}}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right }}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalRelativeDates')} />
					<Switch
						className="big"
						value={showRelativeDates}
						onChange={(e: any, v: boolean) => {
							S.Common.showRelativeDatesSet(v);
							analytics.event('RelativeDates', { type: v });
						}}
					/>
				</div>

				<div className="item">
					<Label text={translate('popupSettingsPersonalFirstDay')} />
					<Select
						id="firstDay"
						value={String(firstDay)}
						options={firstDayOptions}
						onChange={v => S.Common.firstDaySet(v)}
						arrowClassName="black"
						menuParam={{ horizontal: I.MenuDirection.Right }}
					/>
				</div>

			</div>
		</>
	);

});

export default PageMainSettingsLanguage;
